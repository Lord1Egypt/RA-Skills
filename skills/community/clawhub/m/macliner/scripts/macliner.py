#!/usr/bin/python3
"""macliner.py - measure a Mac, plan its cleaning, updates and checks, then do exactly the plan.

  macliner.py plan [--json FILE]        read-only: what would go (with sizes), what needs a choice, what is
                                        out of date, what is wrong, what is never touched; saves the plan
  macliner.py apply [FILE]              does every «auto» line of the saved plan
  macliner.py apply [FILE] --only ID …  does only the named lines («ask», «update», «setting» or «auto»)
  macliner.py remember --yes ID … --no ID … --protect PATH …
                                        keeps standing answers in ~/.config/macliner/answers.json

The plan is saved to FILE, by default macliner-plan.json in the system's temporary folder, and «apply»
reads the same file. A plan older than 3 hours or from another Mac is refused: make a new one.
Deletes for real (no Trash). Every path is checked again against the never-touch list before it goes.
Never asks for a password: lines that need an administrator are printed as commands for the person.
Python 3.9+ standard library and macOS's own commands; Homebrew and mas are used when installed.
Exit codes: 0 done, 1 some lines failed, 2 plan missing, stale or an unknown id, 64 wrong usage.
"""
import datetime as dt
import fnmatch
import glob
import hashlib
import json
import os
import plistlib
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time

HOME = os.path.expanduser("~")
H = lambda p: os.path.join(HOME, p)
ENV = dict(os.environ, PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:" + os.environ.get("PATH", ""),
           HOMEBREW_NO_AUTO_UPDATE="1", HOMEBREW_NO_ENV_HINTS="1", HOMEBREW_NO_ASK="1", NO_COLOR="1", TERM="dumb")
DEFAULT_PLAN = os.path.join(tempfile.gettempdir(), "macliner-plan.json")
ANSWERS = H(".config/macliner/answers.json")
# Until 0.2.0 (2026-11-18) the skill was named mac-clean and kept its answers here: read once if the new file is
# missing; «remember» then writes the new one.
OLD_ANSWERS = H(".config/mac-clean/answers.json")

# Never deleted, whatever a line of the plan says. Globs, matched against the real path and every parent.
# The person's own files and libraries (cannot be recreated), credentials, cloud folders, assistants' own data,
# and what takes hours to get back (virtual machines, simulators, archives, AI models, browsers that tools
# keep in cache folders). A person adds more with «remember --protect PATH».
PROTECTED = [
    H("Desktop"), H("Documents"), H("Library/Mobile Documents"), H("Library/CloudStorage"),
    H("Pictures/*.photoslibrary"), H("Pictures/Photo Booth Library"), H("Music/Music"), H("Music/iTunes"),
    H("Music/GarageBand"), H("Movies/TV"), H("Movies/*.imovielibrary"), H("Movies/*.fcpbundle"),
    H("Library/Mail"), H("Library/Messages"), H("Library/Keychains"), "/Library/Keychains",
    H("Library/Application Support/MobileSync"),                   # iPhone and iPad backups
    H(".ssh"), H(".gnupg"), H(".config"), H(".local"), H(".aws"), H(".kube"), H(".docker"),
    H(".claude"), H(".claude.json"), H(".codex"), H(".gemini"), H(".agents"), H(".cursor"),
    H(".openclaw"), H(".hermes"), H(".opencode"),
    H("Library/Application Support/Claude"), H("Library/Application Support/Code/User"),
    H(".tart"), H("Parallels"), H("Virtual Machines.localized"), H("Library/Containers/com.utmapp.UTM"),
    H("Library/Containers/com.docker.docker"), H(".colima"), H(".orbstack"),
    H("Library/Developer/CoreSimulator"), H("Library/Developer/Xcode/Archives"), H("Library/Developer/Xcode/UserData"),
    "/Applications/Xcode*.app", "/Library/Developer",
    H(".ollama"), H(".lmstudio"), H(".cache/lm-studio"), H(".cache/huggingface"), H(".cache/torch"), H(".cache/whisper"),
    H("Library/Caches/ms-playwright*"), H("Library/Caches/Cypress"), H("Library/Caches/camoufox"), H(".cache/puppeteer"),
    H("Library/Caches/macliner"),
    "/Volumes/*/*",                                                 # files on other disks (their Trash: own line)
    "/System", "/usr", "/bin", "/sbin", "/private/var/db",
]
# Exceptions inside protected globs: the person's own Trash folder on another disk.
UNPROTECTED = ["/Volumes/*/.Trashes/%d/*" % os.getuid()]
# Folders in ~/Library/Caches that are package caches of developer tools: deleting them is safe but the next
# build downloads everything again, so they are a choice, not a sweep.
DEV_CACHES = {"pip", "pypoetry", "Yarn", "go-build", "CocoaPods", "org.carthage.CarthageKit", "node-gyp", "pnpm",
              "deno", "bun", "JetBrains", "composer", "uv", "Homebrew"}
# Apple's own caches without a com.apple. prefix: system services manage them (sync state, maps, wallet).
APPLE_CACHE_NAMES = {"CloudKit", "GeoServices", "PassKit", "FamilyCircle", "Animoji", "AppleMediaServices",
                     "SiriTTS", "Metadata", "CrashReporter"}

T0 = time.time()
ITEMS, NOTES = [], []


# ------------------------------------------------------------------------------------------------- helpers

def run(cmd, timeout=60):
    """Run a command with a hard time limit; never reads stdin. Returns (exit code, stdout+stderr)."""
    try:
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           env=ENV, timeout=timeout, universal_newlines=True, errors="replace")
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        return 124, "timed out after %d s" % timeout
    except OSError as e:
        return 127, "%s: %s" % (cmd[0], e)


def have(tool):
    return shutil.which(tool, path=ENV["PATH"]) is not None


def load_answers():
    try:
        with open(ANSWERS if os.path.exists(ANSWERS) or not os.path.exists(OLD_ANSWERS) else OLD_ANSWERS) as f:
            a = json.load(f)
        return a if isinstance(a, dict) else {}
    except (OSError, ValueError):
        return {}


ANS = load_answers()
PROTECTED += [os.path.expanduser(p) for p in ANS.get("protect", [])]


def protected(path):
    real = os.path.realpath(os.path.expanduser(path))
    for cand in {real, os.path.abspath(os.path.expanduser(path))}:
        if any(fnmatch.fnmatch(cand, u) for u in UNPROTECTED):
            continue
        p = cand
        while p not in ("/", ""):
            if any(fnmatch.fnmatch(p, g) for g in PROTECTED):
                return True
            p = os.path.dirname(p)
    return False


def size_of(path, limit=60):
    """Allocated bytes of a file or folder; None when it could not be read in time."""
    if not os.path.lexists(path):
        return 0
    if os.path.islink(path) or not os.path.isdir(path):
        try:
            return os.lstat(path).st_blocks * 512
        except OSError:
            return None
    end, total, stack = time.time() + limit, 0, [path]
    while stack:
        if time.time() > end:
            return None
        try:
            with os.scandir(stack.pop()) as it:
                for e in it:
                    try:
                        if e.is_dir(follow_symlinks=False):
                            stack.append(e.path)
                        else:
                            total += e.stat(follow_symlinks=False).st_blocks * 512
                    except OSError:
                        pass
        except OSError:
            pass
    return total


def human(n):
    if n is None:
        return "?"
    for unit, k in (("TB", 1e12), ("GB", 1e9), ("MB", 1e6), ("KB", 1e3)):
        if n >= k:
            return "%.1f %s" % (n / k, unit)
    return "%d B" % n


def n_(n, word):
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


def short(p):
    return p.replace(HOME, "~", 1) if p.startswith(HOME) else p


def add(id, cls, title, size=None, paths=(), action=None, why="", detail=()):
    """cls: auto (done without asking), ask (a person's choice), update, setting (left as macOS has it unless the
    person asks), warn (a problem), report (a fact), keep (never touched), ok (a check that is right)."""
    if cls in ("auto", "ask", "setting") and id in ANS.get("no", []):
        cls, title = "keep", title + " (left: standing answer)"
    elif cls in ("ask", "update") and id in ANS.get("yes", []):  # never a setting: its command toggles
        cls, title = "auto", title + " (standing answer: yes)"
    ITEMS.append(dict(id=id, cls=cls, title=title, size=size, paths=list(paths), action=action, why=why,
                      detail=list(detail)))


def listdir(p):
    try:
        return sorted(os.listdir(p))
    except OSError:
        return []


def full_disk_access():
    """Folders macOS guards with Full Disk Access answer «Operation not permitted» without it (no dialog)."""
    for p in (H("Library/Safari"), H("Library/Mail"), H("Library/Messages"), H("Library/Cookies"),
              "/Library/Preferences/com.apple.TimeMachine.plist"):
        if os.path.lexists(p):
            try:
                if os.path.isdir(p):
                    os.listdir(p)
                else:
                    open(p, "rb").close()
                return True
            except PermissionError:
                return False
            except OSError:
                continue
    return False


FDA = full_disk_access() and not os.environ.get("MACLINER_TEST_NO_FDA")


def running_apps():
    """Bundle ids and names of the open apps (lsappinfo: no permission needed)."""
    rc, out = run(["lsappinfo", "list"], 15)
    ids = set(x.lower() for x in re.findall(r'bundleID="([^"]+)"', out))
    names = set(x.lower() for x in re.findall(r'^\s*\d+\) "([^"]+)"', out, re.M))
    return ids, names


RUN_IDS, RUN_NAMES = running_apps()
RUN_VENDORS = {i.split(".")[1] for i in RUN_IDS if i.count(".") >= 2 and not i.startswith("com.apple.")}


def is_open(name):
    n = name.lower()
    return n in RUN_IDS or n in RUN_NAMES or n in RUN_VENDORS


# ------------------------------------------------------------------------------------------------ the sweep

def caches():
    """Regenerable caches of apps (~/Library/Caches and, with Full Disk Access, the apps' own containers)."""
    roots = [H("Library/Caches")]
    if FDA:
        roots += sorted(glob.glob(H("Library/Containers/*/Data/Library/Caches")))
    sweep, dev, big, skipped = [], [], [], []
    for root in roots:
        owner = root.split("/Containers/")[1].split("/")[0] if "/Containers/" in root else None
        if owner and (owner.startswith("com.apple.") or is_open(owner)):
            continue
        for n in listdir(root):
            p = os.path.join(root, n)
            if protected(p) or n.startswith("com.apple.") or n in APPLE_CACHE_NAMES or n.startswith("."):
                continue
            if root == H("Library/Caches") and n in DEV_CACHES:
                dev.append(p)
                continue
            if not owner and is_open(n):
                skipped.append(n)
                continue
            s = size_of(p, 30)
            if s is None:
                continue
            (big if s >= 1e9 else sweep).append((p, s))
    if sweep:
        sweep.sort(key=lambda x: -x[1])
        add("caches", "auto", "App caches: " + n_(len(sweep), "folder"), sum(s for _, s in sweep), [p for p, _ in sweep],
            {"kind": "paths"}, "apps rebuild their caches when needed",
            ["%s  %s" % (human(s), short(p)) for p, s in sweep[:8]]
            + (["skipped, app open: " + ", ".join(sorted(set(skipped)))] if skipped else []))
    for p, s in big:
        add("bigcache:" + os.path.basename(p), "ask", "Large cache: " + short(p), s, [p], {"kind": "paths"},
            "a cache this large may hold something slow to get back (offline media, downloaded models)")
    dev = [(p, size_of(p, 60) or 0) for p in dev if p != H("Library/Caches/Homebrew")]
    for p in (H(".npm/_cacache"), H(".cache/uv"), H(".gradle/caches"), H(".cargo/registry/cache")):
        if os.path.isdir(p) and not protected(p):
            dev.append((p, size_of(p, 60) or 0))
    dev = [(p, s) for p, s in dev if s > 1e6]
    if dev:
        add("dev-caches", "ask", "Package caches of developer tools: " + n_(len(dev), "folder"), sum(s for _, s in dev),
            [p for p, _ in dev], {"kind": "paths"}, "safe to delete, but the next build downloads them again",
            ["%s  %s" % (human(s), short(p)) for p, s in sorted(dev, key=lambda x: -x[1])])


def logs():
    paths = [os.path.join(H("Library/Logs"), n) for n in listdir(H("Library/Logs"))]
    paths = [p for p in paths if not protected(p) and not os.path.basename(p).startswith(".")]
    sized = [(p, size_of(p, 20) or 0) for p in paths]
    if sized:
        add("logs", "auto", "App logs and crash reports: " + n_(len(sized), "item"), sum(s for _, s in sized),
            [p for p, _ in sized], {"kind": "paths"}, "written for debugging; apps start new ones")


def trash():
    if not FDA:
        return
    old, fresh, now = [], [], time.time()
    for n in listdir(H(".Trash")):
        if n == ".DS_Store":
            continue
        p = os.path.join(H(".Trash"), n)
        try:
            moved = os.lstat(p).st_ctime  # moving into the Trash changes ctime: «when it was trashed»
        except OSError:
            continue
        (fresh if now - moved < 86400 else old).append((p, size_of(p, 60) or 0))
    if old:
        add("trash", "auto", "Trash: %s trashed more than a day ago" % n_(len(old), "item"), sum(s for _, s in old),
            [p for p, _ in old], {"kind": "paths"}, "the Trash is where deleted things wait to go")
    if fresh:
        add("trash-new", "ask", "Trash: %s trashed in the last day" % n_(len(fresh), "item"), sum(s for _, s in fresh),
            [p for p, _ in fresh], {"kind": "paths"}, "something trashed minutes ago may still be wanted",
            [os.path.basename(p) for p, _ in fresh][:15])
    uid = str(os.getuid())
    for v in glob.glob("/Volumes/*"):
        t = os.path.join(v, ".Trashes", uid)
        items = [os.path.join(t, n) for n in listdir(t)]
        if items and os.path.realpath(v) != "/":
            add("xtrash:" + os.path.basename(v), "auto", "Trash of the disk «%s»: %s" % (os.path.basename(v),
                n_(len(items), "item")), sum(size_of(p, 60) or 0 for p in items), items, {"kind": "paths", "outside": True})


def homebrew():
    if not have("brew"):
        return
    rc, out = run(["brew", "cleanup", "--prune=all", "-n"], 300)
    m = re.search(r"free approximately ([\d.]+)\s*([KMGT]?B)", out)
    size = int(float(m.group(1)) * {"B": 1, "KB": 1e3, "MB": 1e6, "GB": 1e9, "TB": 1e12}[m.group(2)]) if m else 0
    rc, out2 = run(["brew", "autoremove", "-n"], 120)
    gone = [l.split()[-1] for l in out2.splitlines() if l.strip() and not l.startswith("==>")]
    if size or gone:
        add("brew", "auto", "Homebrew: old versions, downloads" + (", unused dependencies" if gone else ""), size,
            action={"kind": "brew"}, why="installers and old copies of what is installed", detail=gone)


def downloads():
    if not FDA:
        return
    d = H("Downloads")
    partial, installers, old, now = [], [], [], time.time()
    for n in listdir(d):
        p = os.path.join(d, n)
        try:
            st = os.lstat(p)
        except OSError:
            continue
        if re.search(r"\.(download|crdownload|part|partial|opdownload)$", n) and now - st.st_mtime > 3600:
            partial.append(p)
        elif re.search(r"\.(dmg|pkg|mpkg|iso|xip)$", n, re.I):
            installers.append(p)
        elif now - max(st.st_mtime, st.st_ctime) > 90 * 86400:
            old.append(p)
    if partial:
        add("dl-partial", "auto", "Unfinished downloads older than an hour: " + n_(len(partial), "file"),
            sum(size_of(p) or 0 for p in partial), partial, {"kind": "paths"}, "a stopped download never resumes")
    if installers:
        add("dl-installers", "ask", "Installers in Downloads: " + n_(len(installers), "file"),
            sum(size_of(p) or 0 for p in installers), installers, {"kind": "paths"},
            "the app they installed stays; the installer may be kept on purpose",
            [os.path.basename(p) for p in installers][:20])
    if old:
        add("dl-old", "ask", "Untouched for 90 days in Downloads: " + n_(len(old), "item"),
            sum(size_of(p) or 0 for p in old), old, {"kind": "paths"}, "only the person knows what is still needed",
            [os.path.basename(p) for p in old][:20])


def recent_items():
    t = H("Library/Application Support/com.apple.sharedfilelist")
    files = [p for p in glob.glob(t + "/**/*.sfl*", recursive=True)
             if "ApplicationRecentDocuments" in p or re.search(r"LSSharedFileList\.Recent", p)]
    if files:
        add("recent", "ask", "Recent Items lists (documents, apps and servers in the Apple menu and in apps)",
            sum(size_of(p) or 0 for p in files), files, {"kind": "paths", "then": ["killall", "sharedfilelistd"]},
            "privacy: macOS keeps them with no expiry; the lists start empty again")


def safari():
    if not FDA:
        return
    s, c = H("Library/Safari"), H("Library/Containers/com.apple.Safari/Data/Library")
    paths = (glob.glob(s + "/History.db*") + glob.glob(c + "/Cookies/*")
             + [os.path.join(s, x) for x in ("RecentlyClosedTabs.plist", "Downloads.plist", "LocalStorage", "Databases")]
             + [os.path.join(c, x) for x in ("Caches/com.apple.Safari", "Caches/WebKit", "WebKit/WebsiteData")]
             + [H("Library/Caches/com.apple.Safari")])
    paths = [p for p in paths if os.path.lexists(p)]
    if paths:
        op = is_open("com.apple.safari")
        add("safari", "ask", "Safari: history, cookies and website data (signs out of every site; tabs, bookmarks "
            "and passwords stay)" + ("; Safari is open: quit it first" if op else ""),
            sum(size_of(p, 30) or 0 for p in paths), paths,
            {"kind": "paths", "app": "com.apple.Safari", "before": ["pkill", "-x", "com.apple.Safari.History"]},
            "being signed out of every site is the person's call")


def startup():
    """Launch items whose program is gone are leftovers of removed apps; an unsigned program is flagged."""
    for plist in sorted(glob.glob(H("Library/LaunchAgents/*.plist")) + glob.glob("/Library/LaunchAgents/*.plist")
                        + glob.glob("/Library/LaunchDaemons/*.plist")):
        try:
            with open(plist, "rb") as f:
                d = plistlib.load(f)
        except Exception:
            continue
        label = d.get("Label", os.path.basename(plist))
        prog = d.get("Program") or (d.get("ProgramArguments") or [None])[0]
        if not isinstance(prog, str):
            continue
        mine = plist.startswith(HOME)
        if prog.startswith("/") and not os.path.exists(prog):
            add("launch:" + label, "auto", "Starts at login, program gone: %s (%s)" % (label, prog), 0, [plist],
                {"kind": "launch", "outside": not mine}, "a leftover of a removed app")
        elif os.path.isfile(prog) and "Mach-O" in run(["file", "-b", prog], 10)[1] \
                and run(["codesign", "-v", prog], 20)[0] != 0:
            add("launch:" + label, "ask", "Unsigned program starts by itself: %s (%s)" % (label, prog), 0, [plist],
                {"kind": "launch", "outside": not mine}, "unsigned is not proof of harm; the person knows what it is")


def developer():
    ds = H("Library/Developer/Xcode/iOS DeviceSupport")
    models = {}
    for p in glob.glob(ds + "/*"):
        m = re.match(r"(\S+) ([\d.]+)", os.path.basename(p))
        if m:
            models.setdefault(m.group(1), []).append((tuple(int(x) for x in m.group(2).split(".") if x), p))
    old = [p for vs in models.values() for _, p in sorted(vs)[:-1]]
    if old:
        add("xcode-ds", "auto", "Xcode device symbols of older iOS versions: " + n_(len(old), "folder"),
            sum(size_of(p) or 0 for p in old), old, {"kind": "paths"}, "Xcode copies them again from a device if needed",
            [os.path.basename(p) for p in old])
    dd = H("Library/Developer/Xcode/DerivedData")
    s = size_of(dd)
    if s and s > 50e6:
        add("xcode-dd", "auto", "Xcode build cache (DerivedData)", s,
            [os.path.join(dd, x) for x in listdir(dd)], {"kind": "paths"}, "rebuilt on the next build")
    if os.path.isdir(H("Library/Developer/CoreSimulator")) and have("xcrun"):
        rc, out = run(["xcrun", "simctl", "list", "devices", "unavailable"], 60)
        n = len(re.findall(r"\(([0-9A-F-]{36})\)", out))
        if n:
            add("sim-unavailable", "auto", "Simulators whose iOS runtime is gone: %d" % n,
                action={"kind": "cmd", "cmd": ["xcrun", "simctl", "delete", "unavailable"]})


def large_files():
    prune = [H("Library"), H(".Trash")] + [g for g in PROTECTED if g.startswith(HOME + "/")]
    if not FDA:
        prune += [H("Downloads")]
    expr = []
    for g in prune:
        expr += (["-o"] if expr else []) + ["-path", g]
    rc, out = run(["find", HOME, "(", *expr, ")", "-prune", "-o", "-type", "f", "-size", "+1G", "-print"], 300)
    if rc == 124:
        NOTES.append("the search for files over 1 GB timed out; the list may be incomplete")
    for p in out.splitlines():
        if p.startswith("/") and not protected(p):
            add("large:" + short(p), "ask", "Large file: " + short(p), size_of(p), [p], {"kind": "paths"},
                "a file this size is usually there on purpose")


def duplicates():
    """Same content, same size, 1 MB and up, in Downloads, Pictures, Movies, Music (never in libraries)."""
    dirs = [H(x) for x in (("Downloads",) if FDA else ()) + ("Pictures", "Movies", "Music") if os.path.isdir(H(x))]
    by_size, end = {}, time.time() + 240
    for d in dirs:
        for root, subdirs, files in os.walk(d):
            subdirs[:] = [s for s in subdirs if not protected(os.path.join(root, s)) and not s.startswith(".")
                          and not s.endswith((".app", ".photoslibrary", ".bundle"))]
            for n in files:
                p = os.path.join(root, n)
                try:
                    st = os.lstat(p)
                except OSError:
                    continue
                if st.st_size >= 1e6 and not os.path.islink(p):
                    by_size.setdefault(st.st_size, []).append(p)
            if time.time() > end:
                NOTES.append("the duplicate search stopped after 4 minutes; the list may be incomplete")
                break

    def digest(p, head=None):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            if head:
                h.update(f.read(head))
            else:
                for b in iter(lambda: f.read(1 << 20), b""):
                    h.update(b)
        return h.hexdigest()

    groups = []
    for size, ps in by_size.items():
        if len(ps) < 2:
            continue
        for stage in (65536, None):
            buckets = {}
            for p in ps:
                try:
                    buckets.setdefault(digest(p, stage), []).append(p)
                except OSError:
                    pass
            ps = [p for b in buckets.values() if len(b) > 1 for p in b]
            if stage is None:
                groups += [(k, size, b) for k, b in buckets.items() if len(b) > 1]
            if not ps:
                break
    for key, size, ps in sorted(groups, key=lambda g: -g[1] * (len(g[2]) - 1)):
        ps.sort(key=lambda p: (os.lstat(p).st_mtime, len(p)))  # the oldest copy stays: the original
        add("dup:" + key[:10], "ask", "Duplicate: %d copies of %s" % (len(ps), os.path.basename(ps[0])),
            size * (len(ps) - 1), ps[1:], {"kind": "paths"}, "which copy stays is the person's choice",
            ["stays: " + short(ps[0])] + ["goes:  " + short(p) for p in ps[1:]])


def installed():
    """Bundle id -> app path, for every app Spotlight and the Applications folders know."""
    rc, out = run(["mdfind", "kMDItemContentType == 'com.apple.application-bundle'"], 60)
    apps = set(out.splitlines()) | set(glob.glob("/Applications/*.app")) | set(glob.glob("/Applications/*/*.app")) \
        | set(glob.glob(H("Applications/*.app")))
    ids = {}
    for a in apps:
        try:
            with open(os.path.join(a, "Contents/Info.plist"), "rb") as f:
                i = plistlib.load(f).get("CFBundleIdentifier")
            if i:
                ids[i.lower()] = a
        except Exception:
            pass
    return ids


APPS = installed()


def app_data(bid, name):
    """Where an app keeps its data in the home folder, by bundle id (and by name in Application Support)."""
    L = H("Library")
    cands = [L + "/Containers/" + bid, L + "/Application Support/" + bid, L + "/Application Support/" + name,
             L + "/Caches/" + bid, L + "/HTTPStorages/" + bid, L + "/WebKit/" + bid, L + "/Logs/" + name,
             L + "/Preferences/" + bid + ".plist", L + "/Saved Application State/" + bid + ".savedState"]
    cands += glob.glob(L + "/Group Containers/*." + bid)
    if not FDA:
        cands = [c for c in cands if "/Containers/" not in c]
    return [c for c in cands if os.path.lexists(c) and not protected(c)]


def orphans():
    """Data in ~/Library named after an app id whose vendor has no app installed any more."""
    vendors = {".".join(i.split(".")[:2]) for i in APPS}
    roots = ["Application Support", "HTTPStorages", "WebKit", "Saved Application State", "Preferences"]  # Caches: swept
    if FDA:
        roots += ["Containers", "Group Containers"]
    found = {}
    for r in roots:
        base = H("Library/" + r)
        for n in listdir(base):
            key = re.sub(r"\.(plist|savedState|binarycookies)$", "", n)
            key = re.sub(r"^[A-Z0-9]{10}\.", "", key)  # team id in front of group containers
            key = re.sub(r"^group\.", "", key).lower()
            parts = key.split(".")
            if len(parts) < 3 or parts[0] not in ("com", "org", "net", "io", "app", "dev", "co", "me", "tv", "de", "uk"):
                continue
            if key.startswith("com.apple.") or ".".join(parts[:2]) in vendors:
                continue
            p = os.path.join(base, n)
            if not protected(p):
                found.setdefault(".".join(parts[:3]), []).append(p)
    for key, paths in sorted(found.items()):
        s = sum(size_of(p, 30) or 0 for p in paths)
        if s >= 1e6:
            add("orphan:" + key, "ask", "Data of an app that is not installed: %s (%s)" % (key, n_(len(paths), "place")), s,
                paths, {"kind": "paths"}, "a command-line tool or a helper can use an app-like name; check before",
                [short(p) for p in paths])


def unused_apps():
    casks = {}
    if have("brew"):
        rc, out = run(["brew", "info", "--cask", "--installed", "--json=v2"], 120)
        try:
            for c in json.loads(out[out.index("{"):])["casks"]:
                for art in c.get("artifacts", []):
                    for a in (art.get("app", []) if isinstance(art, dict) else []):
                        casks[a["target"] if isinstance(a, dict) else a] = c["token"]
        except (ValueError, KeyError, TypeError):
            pass
    cutoff = time.time() - 180 * 86400
    for a in sorted(glob.glob("/Applications/*.app")):
        name = os.path.basename(a)
        try:
            with open(os.path.join(a, "Contents/Info.plist"), "rb") as f:
                bid = plistlib.load(f).get("CFBundleIdentifier", "")
        except Exception:
            continue
        if not bid or bid.startswith("com.apple.") or name.startswith("Xcode") or protected(a):
            continue
        rc, out = run(["mdls", "-raw", "-name", "kMDItemLastUsedDate", a], 10)
        m = re.match(r"(\d{4}-\d\d-\d\d)", out.strip())  # «2026-11-17 6:14:00 PM +0000», a narrow space before PM
        used = time.mktime(time.strptime(m.group(1), "%Y-%m-%d")) if m else None
        if used is not None and used >= cutoff:
            continue
        data = app_data(bid, name[:-4])
        store = os.path.isdir(os.path.join(a, "Contents/_MASReceipt"))
        how = ("brew uninstall --cask " + casks[name]) if name in casks else ("App Store app" if store else "deleted")
        when = "never opened" if used is None else "last opened " + time.strftime("%Y-%m-%d", time.localtime(used))
        add("app:" + name, "ask", "App %s: %s" % (when, name), (size_of(a, 60) or 0) + sum(size_of(p, 30) or 0 for p in data),
            [a] + data, {"kind": "app", "app": bid, "cask": casks.get(name), "outside": not os.access(a, os.W_OK)},
            "removing an app and its data is the person's choice",
            ["removed by: " + how] + ["with its data: " + short(p) for p in data])


# ----------------------------------------------------------------------------------- updates and security

def updates():
    if have("brew"):
        rc, out = run(["brew", "outdated", "--json=v2"], 120)
        try:
            j = json.loads(out[out.index("{"):])
            iv = lambda x: x["installed_versions"][-1] if isinstance(x["installed_versions"], list) else x["installed_versions"]
            lines = ["%s %s -> %s" % (x["name"], iv(x), x["current_version"]) for x in j["formulae"] + j["casks"]]
            if lines:
                add("upd-brew", "update", "Homebrew updates: %d" % len(lines), detail=lines, action={"kind": "brew-upgrade"},
                    why="as of the last «brew update»; apply runs it first, so the list can grow")
        except (ValueError, KeyError):
            add("upd-brew", "warn", "Homebrew: the list of updates could not be read", detail=[out[-300:]])
    if have("mas"):
        rc, out = run(["mas", "outdated"], 120)
        if rc == 0 and out.strip():
            add("upd-mas", "update", "App Store updates", detail=out.strip().splitlines(),
                action={"kind": "cmd", "cmd": ["sudo", "mas", "upgrade"]})
        elif rc == 0:
            add("upd-mas-ok", "ok", "App Store apps are up to date (checked with mas)")
        else:
            add("upd-mas-err", "warn", "App Store: mas could not list updates", detail=[out.strip()[-300:]])
    else:
        add("upd-mas-none", "report", "App Store updates were not checked: the mas tool is not installed" +
            (" (optional: brew install mas)" if have("brew") else " (it is installed with Homebrew, which is not installed either)"))
    rc, out = run(["softwareupdate", "--list"], 180)
    labels = re.findall(r"\* Label: (.*)", out)
    if labels:
        add("upd-macos", "report", "macOS updates waiting: install them in System Settings > General > Software Update "
            "(the Mac restarts)", detail=labels)
    elif rc == 124:
        add("upd-macos", "warn", "The macOS update check timed out (network?)")
    else:
        add("upd-macos", "ok", "macOS is up to date")


def rd(dom, key, host=False):
    rc, out = run(["defaults"] + (["-currentHost"] if host else []) + ["read", dom, key], 10)
    return out.strip() if rc == 0 else None


def security():
    fw = "/usr/libexec/ApplicationFirewall/socketfilterfw"
    su = "/Library/Preferences/com.apple.SoftwareUpdate"
    chk = lambda id, good, title: add(id, "ok" if good else "warn", title)
    chk("sec-sip", "enabled." in run(["csrutil", "status"], 10)[1], "System Integrity Protection on")
    chk("sec-gk", "assessments enabled" in run(["spctl", "--status"], 10)[1], "Gatekeeper on")
    chk("sec-fv", "FileVault is On" in run(["fdesetup", "status"], 10)[1], "FileVault disk encryption on")
    m = re.search(r"Version: (\d+) Installed: (\d{4}-\d\d-\d\d)", run(["xprotect", "version"], 20)[1])
    if m:
        age = (dt.date.today() - dt.date(*map(int, m.group(2).split("-")))).days
        chk("sec-xprotect", age <= 30, "XProtect malware definitions %s, %d days old" % (m.group(1), age))
    chk("sec-rsr", rd(su, "CriticalUpdateInstall") != "0" and rd(su, "ConfigDataInstall") != "0",
        "Security responses and system data files install automatically")
    chk("sec-autologin", rd("/Library/Preferences/com.apple.loginwindow", "autoLoginUser") is None,
        "No automatic login")
    chk("sec-guest", rd("/Library/Preferences/com.apple.loginwindow", "GuestEnabled") != "1", "Guest user off")
    m = re.search(r"screenLock delay is (.*)", run(["sysadminctl", "-screenLock", "status"], 10)[1])
    if m:
        d = m.group(1).strip()
        chk("sec-lock", d == "immediate" or bool(re.match(r"\d+ seconds", d)), "Password after sleep or screen saver: " + d)
    out = run(["profiles", "status", "-type", "enrollment"], 15)[1]
    if "MDM enrollment: Yes" in out:
        add("sec-mdm", "report", "The Mac is managed by an organisation (MDM): its settings may be set by them")

    rc, out = run(["netstat", "-anv", "-p", "tcp"], 15)
    listen = sorted({(m.group(1), m.group(2)) for m in
                     re.finditer(r"^tcp\S*\s+\d+\s+\d+\s+\S*?[.:](\d+)\s+\S+\s+LISTEN\s.*?\s(\S+?):\d+\s", out, re.M)
                     if not re.match(r"(127\.|::1|localhost)", m.group(0).split()[3])})
    if listen:
        add("net-listen", "report", "Programs that accept connections from the network",
            detail=["%s on port %s" % (p, port) for port, p in listen], why="the firewall decides who reaches them")

    # Settings that trade comfort for safety or privacy. The baseline is how macOS ships: the plan names each
    # one as a fact with its trade-off and changes it only when the person asks («apply --only ID»).
    fw_on = "enabled" in run([fw, "--getglobalstate"], 10)[1]
    stealth = "stealth mode is on" in run([fw, "--getstealthmode"], 10)[1]
    airplay = any(p.startswith("ControlCe") for port, p in listen if port in ("5000", "7000"))
    analytics = rd("/Library/Application Support/CrashReporter/DiagnosticMessagesHistory.plist", "AutoSubmit") == "1"
    auto_macos = rd(su, "AutomaticallyInstallMacOSUpdates") == "1"
    smb = any(p == "smbd" for _, p in listen)
    ssh = any(port == "22" for port, _ in listen)
    s = "System Settings > "
    for id, state, title, trade, cmd in [
        ("firewall", fw_on, "Firewall", "on: blocks unknown incoming connections, may ask about an app; macOS ships it off",
         ["sudo", fw, "--setglobalstate", "off" if fw_on else "on"]),
        ("stealth", stealth, "Firewall stealth mode", "on: the Mac does not answer pings, harder to find on public Wi-Fi; "
         "off by default", ["sudo", fw, "--setstealthmode", "off" if stealth else "on"]),
        ("airplay", airplay, "AirPlay Receiver", "on (as shipped): phones on the same network can play to this Mac; off "
         "closes ports 5000 and 7000. " + s + "General > AirDrop & Handoff", None),
        ("analytics", analytics, "Share Mac Analytics with Apple", "a choice made at setup. " + s +
         "Privacy & Security > Analytics & Improvements", None),
        ("macos-auto", auto_macos, "Install macOS updates automatically", "on: macOS may install and restart overnight; "
         "off: the person installs them. " + s + "General > Software Update > Automatic Updates", None),
        ("file-sharing", smb, "File Sharing", "on: others on the network can open shared folders. " + s +
         "General > Sharing", None),
        ("remote-login", ssh, "Remote Login (SSH)", "on: others can sign in to this Mac over the network. " + s +
         "General > Sharing", None),
    ]:
        add("set:" + id, "setting", "%s: %s" % (title, "on" if state else "off"), why=trade,
            action={"kind": "cmd", "cmd": cmd} if cmd else None)
    rc, out = run(["sharing", "-l"], 10)
    names = re.findall(r"^name:\s+(.*)$", out, re.M)
    if names:
        add("net-shares", "report", "Shared folders: %s (File Sharing %s)" % (", ".join(names), "on" if smb else "off"))


def hardware():
    out = run(["system_profiler", "SPPowerDataType"], 30)[1]
    cyc = re.search(r"Cycle Count: (\d+)", out)
    cond = re.search(r"Condition: (.+)", out)
    cap = re.search(r"Maximum Capacity: (\d+)%", out)
    if cyc or cap:
        c = int(cap.group(1)) if cap else None
        good = (c is None or c >= 80) and (not cond or cond.group(1).strip() == "Normal")
        add("hw-battery", "ok" if good else "warn", "Battery: %s cycles, %s capacity%s" % (
            cyc.group(1) if cyc else "?", "%d %%" % c if c is not None else "?",
            ", " + cond.group(1).strip() if cond else ""))
    out = run(["diskutil", "info", "disk0"], 20)[1]
    m = re.search(r"SMART Status:\s+(.+)", out)
    if m:
        add("hw-ssd", "ok" if m.group(1).strip() == "Verified" else "warn", "Internal disk SMART status: " + m.group(1).strip())
    out = run(["pmset", "-g", "therm"], 10)[1]
    m = re.search(r"CPU_Speed_Limit\s*=\s*(\d+)", out)
    add("hw-thermal", "warn" if m and int(m.group(1)) < 100 else "ok",
        "CPU slowed by heat to %s %%" % m.group(1) if m and int(m.group(1)) < 100 else "No slowing by heat recorded")
    n = 0
    for d in ("/Library/Logs/DiagnosticReports", H("Library/Logs/DiagnosticReports")):
        for p in listdir(d):
            if p.endswith(".panic") or (p.startswith("Kernel") and p.endswith(".ips")):
                try:
                    n += time.time() - os.lstat(os.path.join(d, p)).st_mtime < 30 * 86400
                except OSError:
                    pass
    add("hw-panics", "warn" if n else "ok", "Kernel panics (sudden restarts) in 30 days: %d" % n)


def keep_list():
    for p, title in [("Pictures/Photos Library.photoslibrary", "Photos library"), ("Library/Mail", "Mail"),
                     ("Library/Messages", "Messages"), ("Library/Mobile Documents", "iCloud Drive (local copies)"),
                     ("Library/Application Support/MobileSync/Backup", "iPhone and iPad backups"),
                     ("Library/Developer/CoreSimulator", "Xcode simulators"),
                     ("Library/Developer/Xcode/Archives", "Xcode archives"), (".ollama", "Ollama models"),
                     (".cache/huggingface", "Hugging Face models"), (".lmstudio", "LM Studio models"),
                     (".tart", "Tart virtual machines"), ("Parallels", "Parallels virtual machines"),
                     ("Library/Containers/com.docker.docker", "Docker Desktop disk")]:
        q = H(p)
        if os.path.exists(q) and (FDA or "/Containers/" not in q and "Library/M" not in q):
            rc, out = run(["du", "-sk", q], 120)
            m = re.match(r"(\d+)", out)
            if m and int(m.group(1)) > 0:
                add("keep:" + p, "keep", title + " (" + short(q) + ")", int(m.group(1)) * 1024)
    rc, out = run(["tmutil", "listlocalsnapshots", "/"], 20)
    n = len([l for l in out.splitlines() if "com.apple.TimeMachine" in l])
    if n:
        add("tm-snapshots", "report", "Time Machine local snapshots: %d (macOS frees their space by itself when the disk "
            "fills; Finder counts it as «purgeable»)" % n)


# --------------------------------------------------------------------------------------------------- plan

def free_bytes():
    for v in ("/System/Volumes/Data", "/"):
        try:
            st = os.statvfs(v)
            return st.f_bavail * st.f_frsize
        except OSError:
            pass
    return 0


ORDER = [("auto", "Done without asking"), ("ask", "Needs the person's choice"), ("update", "Updates"),
         ("warn", "Problems found"), ("setting", "Settings, left as they are unless the person asks"),
         ("report", "Facts"), ("keep", "Never touched"), ("ok", "Already right")]


def print_plan(plan):
    out = ["macliner plan  %s  %s  macOS %s  free %s  (%d s, nothing changed)" % (
        plan["date"], plan["host"], plan["macos"], human(plan["free"]), plan["seconds"])]
    for cls, title in ORDER:
        items = [i for i in plan["items"] if i["cls"] == cls]
        if not items:
            continue
        total = sum(i["size"] or 0 for i in items)
        out.append("\n== %s%s" % (title, "  (%s)" % human(total) if cls in ("auto", "ask") and total else ""))
        for i in items:
            sz = "%9s  " % human(i["size"]) if i["size"] else " " * 11
            out.append("  %s%s   [%s]" % (sz, i["title"], i["id"]))
            for d in i["detail"][:12]:
                out.append(" " * 13 + "- " + d)
            if len(i["detail"]) > 12:
                out.append(" " * 13 + "- ... %d more" % (len(i["detail"]) - 12))
            if i["why"] and cls in ("ask", "setting"):
                out.append(" " * 13 + "(" + i["why"] + ")")
    for n in plan["notes"]:
        out.append("\nNote: " + n)
    out.append("\nPlan saved: " + plan["file"])
    return "\n".join(out)


def make_plan(path):
    if not FDA:
        NOTES.append("Full Disk Access is off for the app running this, so Downloads, the Trash, Safari and the apps' "
                     "own containers were not read. To include them: System Settings > Privacy & Security > Full Disk "
                     "Access, turn it on for that app (the terminal or the assistant's app), reopen it, plan again.")
    else:
        NOTES.append("Full Disk Access is on: Downloads, the Trash, Safari and the apps' own containers were read.")
    empty = []
    for fn in (caches, logs, trash, homebrew, downloads, recent_items, safari, startup, developer, large_files,
               duplicates, orphans, unused_apps, updates, security, hardware, keep_list):
        t = time.time()
        n = len(ITEMS)
        try:
            fn()
        except Exception as e:  # one broken step must not hide the rest of the plan
            add("error:" + fn.__name__, "warn", "This check failed: %s: %r" % (fn.__name__, e))
        if time.time() - t > 120:
            NOTES.append("slow step: %s took %d s" % (fn.__name__, time.time() - t))
        if len(ITEMS) == n and fn.__name__ != "keep_list":
            empty.append(fn.__name__.replace("_", " "))
    if empty:  # so a group missing from the plan reads as checked and empty, not as skipped
        NOTES.append("Checked, nothing found: " + ", ".join(empty) + ".")
    seen = {}
    for i in ITEMS:  # ids must be unique for --only
        if i["id"] in seen:
            seen[i["id"]] += 1
            i["id"] += "#%d" % seen[i["id"]]
        else:
            seen[i["id"]] = 1
    plan = dict(date=time.strftime("%Y-%m-%d %H:%M"), host=socket.gethostname(),
                macos=run(["sw_vers", "-productVersion"], 5)[1].strip(), free=free_bytes(),
                seconds=int(time.time() - T0), notes=NOTES, items=ITEMS, file=path, fda=FDA)
    with open(path, "w") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    print(print_plan(plan))
    return 0


# -------------------------------------------------------------------------------------------------- apply

def delete(path):
    """Delete one path for real after the never-touch check; raises when something could not go."""
    if protected(path):
        raise PermissionError("never-touch list, not deleted: " + short(path))
    if not os.path.lexists(path):
        return
    if os.path.isdir(path) and not os.path.islink(path):
        errs = []
        shutil.rmtree(path, onerror=lambda f, p, e: errs.append(p))
        if errs:
            raise PermissionError("%d files could not be deleted in %s" % (len(errs), short(path)))
    else:
        os.remove(path)


def sudo_ok():
    return run(["sudo", "-n", "true"], 10)[0] == 0


def apply(path, only):
    try:
        with open(path) as f:
            plan = json.load(f)
    except (OSError, ValueError):
        print("no plan at %s: run «macliner.py plan» first" % path)
        return 2
    age = time.time() - time.mktime(time.strptime(plan["date"], "%Y-%m-%d %H:%M"))
    if age > 3 * 3600 or plan["host"] != socket.gethostname():
        print("the plan is older than 3 hours or from another Mac: run «macliner.py plan» again")
        return 2
    ids = {i["id"] for i in plan["items"]}
    unknown = [x for x in only if x not in ids]
    if unknown:
        print("not in the plan: " + ", ".join(unknown) + "  (ids are the words in [brackets] of the plan)")
        return 2
    if only:
        chosen = [i for i in plan["items"] if i["id"] in only]
    else:
        chosen = [i for i in plan["items"] if i["cls"] == "auto"]
    admin, done, failed, skipped = sudo_ok(), [], [], []
    need_admin = []
    open_ids, open_names = running_apps()
    free0 = free_bytes()
    for i in chosen:
        a = i.get("action")
        if not a:
            skipped.append("%s: nothing to run here (%s)" % (i["id"], i["why"] or "a fact"))
            continue
        k = a["kind"]
        try:
            if a.get("app") and a["app"].lower() in open_ids:
                skipped.append("%s: the app is open; quit it and run this line again" % i["id"])
                continue
            if k == "paths":
                if a.get("before"):
                    run(a["before"], 10)
                    time.sleep(1)
                errs = []
                for p in i["paths"]:
                    try:
                        delete(p)
                    except OSError as e:
                        errs.append(str(e))
                if a.get("then"):
                    run(a["then"], 10)
                if errs:
                    raise RuntimeError("; ".join(errs[:3]) + (" (+%d more)" % (len(errs) - 3) if len(errs) > 3 else ""))
            elif k == "brew":
                for cmd in (["brew", "autoremove"], ["brew", "cleanup", "--prune=all"]):
                    rc, out = run(cmd, 900)
                    if rc:
                        raise RuntimeError("%s: exit %d: %s" % (" ".join(cmd), rc, out[-300:]))
            elif k == "brew-upgrade":
                rc, out = run(["brew", "update"], 600)
                if rc:
                    raise RuntimeError("brew update: exit %d: %s" % (rc, out[-300:]))
                # An open app's cask is held back: upgrading it quits the app (it could be the assistant itself).
                rc, out = run(["brew", "outdated", "--cask", "--quiet"], 120)
                held = []
                for token in out.split():
                    rc2, info = run(["brew", "info", "--cask", "--json=v2", token], 60)
                    apps = re.findall(r'"app":\s*\[\s*"([^"]+\.app)"', info) + re.findall(r'"target":\s*"([^"]+\.app)"', info)
                    if any(x[:-4].lower() in open_names for x in apps):
                        held.append(token)
                rc, out = run(["brew", "upgrade", "--formula"], 1800)
                if rc:
                    raise RuntimeError("brew upgrade --formula: exit %d: %s" % (rc, out[-300:]))
                rest = [t for t in run(["brew", "outdated", "--cask", "--quiet"], 120)[1].split() if t not in held]
                if rest:
                    rc, out = run(["brew", "upgrade", "--cask"] + rest, 1800)
                    if rc:
                        raise RuntimeError("brew upgrade --cask: exit %d: %s" % (rc, out[-300:]))
                if held:
                    skipped.append("upd-brew: held because the app is open: " + ", ".join(held))
            elif k == "cmd":
                cmd = a["cmd"]
                if cmd[0] == "sudo":
                    if not admin:
                        need_admin.append(" ".join(cmd))
                        continue
                    cmd = ["sudo", "-n"] + cmd[1:]
                rc, out = run(cmd, 1800)
                if rc:
                    raise RuntimeError("exit %d: %s" % (rc, out[-300:]))
            elif k == "launch":
                p = i["paths"][0]
                if a.get("outside"):
                    dom = "gui/%d" % os.getuid() if p.startswith("/Library/LaunchAgents") else "system"
                    cmds = [["sudo", "launchctl", "bootout", dom, p], ["sudo", "rm", "-f", p]]
                    if not admin:
                        need_admin.append(" ; ".join(" ".join(c) for c in cmds))
                        continue
                    run(["sudo", "-n"] + cmds[0][1:], 20)
                    rc, out = run(["sudo", "-n"] + cmds[1][1:], 20)
                    if rc:
                        raise RuntimeError(out[-200:])
                else:
                    run(["launchctl", "bootout", "gui/%d" % os.getuid(), p], 20)
                    delete(p)
            elif k == "app":
                app = i["paths"][0]
                if a.get("cask"):
                    rc, out = run(["brew", "uninstall", "--cask", a["cask"]], 600)
                    if rc:
                        raise RuntimeError("brew uninstall: " + out[-300:])
                elif a.get("outside"):
                    if not admin:
                        need_admin.append("sudo rm -rf '%s'" % app)
                    else:
                        rc, out = run(["sudo", "-n", "rm", "-rf", app], 120)
                        if rc:
                            raise RuntimeError(out[-200:])
                else:
                    delete(app)
                for p in i["paths"][1:]:
                    delete(p)
            else:
                raise RuntimeError("unknown action " + k)
            done.append(i["id"])
        except Exception as e:
            failed.append("%s: %s" % (i["id"], e))
    freed = free_bytes() - free0
    print("done %d, failed %d, skipped %d; free space now %s (%s%s)" % (
        len(done), len(failed), len(skipped) + len(need_admin), human(free_bytes()), "+" if freed >= 0 else "-",
        human(abs(freed))))
    for f in failed:
        print("  failed: " + f)
    for s in skipped:
        print("  skipped: " + s)
    if need_admin:
        print("  needs an administrator; the person can paste these into Terminal:")
        for c in need_admin:
            print("    " + c)
    print("verify: run «macliner.py plan» again; every line done must be gone from it")
    return 1 if failed else 0


def remember(argv):
    a = load_answers()
    key = None
    for x in argv:
        if x in ("--yes", "--no", "--protect"):
            key = x[2:]
        elif key:
            v = os.path.abspath(os.path.expanduser(x)) if key == "protect" else x
            lst = a.setdefault(key, [])
            if v not in lst:
                lst.append(v)
            other = {"yes": "no", "no": "yes"}.get(key)
            if other and v in a.get(other, []):
                a[other].remove(v)
        else:
            print("usage: macliner.py remember --yes ID ... --no ID ... --protect PATH ...", file=sys.stderr)
            return 64
    os.makedirs(os.path.dirname(ANSWERS), exist_ok=True)
    a["_about"] = ("Standing answers of the macliner skill: «yes» ids are done without asking, «no» ids are left, "
                   "«protect» paths are never deleted. Edit or delete this file at will.")
    with open(ANSWERS, "w") as f:
        json.dump(a, f, ensure_ascii=False, indent=1)
    print("saved: " + ANSWERS)
    return 0


def arg(argv, flag):
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv):
            return argv[i + 1]
    return None


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    if sys.platform != "darwin":
        print("this script runs only on macOS", file=sys.stderr)
        return 64
    if argv[0] == "plan":
        return make_plan(os.path.abspath(arg(argv, "--json") or DEFAULT_PLAN))
    if argv[0] == "apply":
        rest = argv[1:]
        only = rest[rest.index("--only") + 1:] if "--only" in rest else []
        rest = rest[:rest.index("--only")] if "--only" in rest else rest
        if "--yes" in rest:
            print("use --only ID ... to name the lines to do", file=sys.stderr)
            return 64
        return apply(os.path.abspath(rest[0]) if rest else DEFAULT_PLAN, only)
    if argv[0] == "remember":
        return remember(argv[1:])
    print("usage: macliner.py plan [--json FILE] | apply [FILE] [--only ID ...] | remember ... (--help)", file=sys.stderr)
    return 64


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        print("\ninterrupted")
        sys.exit(130)
