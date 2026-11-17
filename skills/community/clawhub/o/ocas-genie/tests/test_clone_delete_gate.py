#!/usr/bin/env python3
"""Regression tests for genie's clone-deletion safety gate.

History: clean_git_clones deleted any sufficiently old clone that merely had a
remote configured. It never checked for uncommitted changes, stashes, or
unpushed commits — though SKILL.md documented all of those as required gates.
On 2026-08-16 it destroyed a real clone on a production box.

An adversarial audit of the first fix found four more ways for the only copy of
something to be deleted: git-ignored files (.env) are invisible to
`git status --porcelain`; commits held only by a tag belong to no branch;
and remote-tracking refs are a LOCAL CACHE, so a branch deleted upstream — or a
remote repository that no longer exists — still read as "fully pushed".

Every case below is a scenario where deletion would destroy data that exists
nowhere else. Run: python3 tests/test_clone_delete_gate.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import genie  # noqa: E402

FAILURES = []


def sh(*args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)


def git(repo, *args):
    sh("git", "-C", repo, *args)


def make_clone(root, name, origin):
    path = os.path.join(root, name)
    sh("git", "clone", "-q", origin, path)
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "test")
    return path


def write(path, name, text):
    with open(os.path.join(path, name), "w") as fh:
        fh.write(text)


def check(label, blockers, expect_safe, expect_substr=None):
    if expect_safe:
        ok = blockers == []
    else:
        ok = bool(blockers) and (expect_substr is None or
                                 any(expect_substr in b for b in blockers))
    print("%-34s %-6s %s" % (label, "PASS" if ok else "FAIL", blockers))
    if not ok:
        FAILURES.append(label)


def main():
    root = tempfile.mkdtemp(prefix="genie-gate-")
    try:
        origin = os.path.join(root, "origin.git")
        sh("git", "init", "-q", "--bare", "-b", "main", origin)

        seed = make_clone(root, "seed", origin)
        write(seed, "f.txt", "hello\n")
        write(seed, ".gitignore", ".env\ndata/\nnode_modules/\n")
        git(seed, "add", "-A")
        git(seed, "commit", "-q", "-m", "init")
        git(seed, "push", "-q", "-u", "origin", "main")

        # 1. clean + fully pushed -> deletable
        clean = make_clone(root, "clean", origin)
        check("clean+pushed", genie.clone_delete_blockers(clean), True)

        # 2. uncommitted working-tree change -> blocked
        dirty = make_clone(root, "dirty", origin)
        write(dirty, "f.txt", "hello\nlocal edit\n")
        check("uncommitted change", genie.clone_delete_blockers(dirty), False, "uncommitted")

        # 3. committed but unpushed -> blocked
        unpushed = make_clone(root, "unpushed", origin)
        write(unpushed, "new.txt", "work that exists only here\n")
        git(unpushed, "add", "new.txt")
        git(unpushed, "commit", "-q", "-m", "local only")
        check("unpushed commit", genie.clone_delete_blockers(unpushed), False, "unpushed")

        # 4. branch with no upstream -> unverifiable, blocked
        noup = make_clone(root, "noup", origin)
        git(noup, "checkout", "-q", "-b", "feature")
        check("branch without upstream", genie.clone_delete_blockers(noup), False, "no upstream")

        # 5. stashed work -> blocked
        stashed = make_clone(root, "stashed", origin)
        write(stashed, "f.txt", "hello\nstash me\n")
        git(stashed, "stash")
        check("stashed work", genie.clone_delete_blockers(stashed), False, "stash")

        # 6. not a git repo -> fails closed
        plain = os.path.join(root, "plain")
        os.makedirs(plain)
        check("not a repo (fail closed)", genie.clone_delete_blockers(plain), False)

        # 7. protected path -> blocked even when clean
        check("protected path", genie.clone_delete_blockers(clean, ["clean"]), False, "protected")

        # 8. detached HEAD with a local commit -> blocked (no branch holds it)
        detached = make_clone(root, "detached", origin)
        git(detached, "checkout", "-q", "--detach")
        write(detached, "detached.txt", "work reachable from no branch\n")
        git(detached, "add", "detached.txt")
        git(detached, "commit", "-q", "-m", "detached work")
        check("detached HEAD", genie.clone_delete_blockers(detached), False, "detached")

        # 9. git-ignored file holding the only copy of a secret -> blocked
        ignored = make_clone(root, "ignored", origin)
        write(ignored, ".env", "PROD_KEY=only-copy-in-existence\n")
        check("ignored .env is precious", genie.clone_delete_blockers(ignored), False, "git-ignored")

        # 10. only rebuildable ignored content -> still deletable
        rebuildable = make_clone(root, "rebuildable", origin)
        os.makedirs(os.path.join(rebuildable, "node_modules", "pkg"))
        write(rebuildable, "node_modules/pkg/index.js", "module.exports=1\n")
        check("node_modules is disposable", genie.clone_delete_blockers(rebuildable), True)

        # 11. commit held only by a tag (branch reset away) -> blocked
        tagged = make_clone(root, "tagged", origin)
        write(tagged, "rescue.txt", "irreplaceable\n")
        git(tagged, "add", "rescue.txt")
        git(tagged, "commit", "-q", "-m", "tagged work")
        git(tagged, "tag", "v-rescue")
        git(tagged, "reset", "-q", "--hard", "HEAD~1")
        check("tag-only commit", genie.clone_delete_blockers(tagged), False, "no remote-tracking ref")

        # 12. upstream branch deleted on the remote -> blocked
        gone_branch = make_clone(root, "gone-branch", origin)
        git(gone_branch, "checkout", "-q", "-b", "feature")
        write(gone_branch, "feature.txt", "shipped then deleted upstream\n")
        git(gone_branch, "add", "feature.txt")
        git(gone_branch, "commit", "-q", "-m", "feature")
        git(gone_branch, "push", "-q", "-u", "origin", "feature")
        sh("git", "-C", origin, "update-ref", "-d", "refs/heads/feature")
        check("upstream branch deleted", genie.clone_delete_blockers(gone_branch),
              False, "no longer exists on the remote")

        # 13. the remote repository itself is gone -> blocked
        orphan_origin = os.path.join(root, "orphan.git")
        sh("git", "init", "-q", "--bare", "-b", "main", orphan_origin)
        orphan_seed = make_clone(root, "orphan-seed", orphan_origin)
        write(orphan_seed, "f.txt", "x\n")
        git(orphan_seed, "add", "-A")
        git(orphan_seed, "commit", "-q", "-m", "init")
        git(orphan_seed, "push", "-q", "-u", "origin", "main")
        orphan = make_clone(root, "orphan", orphan_origin)
        shutil.rmtree(orphan_origin)
        check("remote repo deleted", genie.clone_delete_blockers(orphan), False, "remote unreachable")

        # 14. GIT_DIR in the environment must not redirect the probes
        env_victim = make_clone(root, "env-victim", origin)
        write(env_victim, "f.txt", "hello\nuncommitted\n")
        os.environ["GIT_DIR"] = os.path.join(clean, ".git")
        os.environ["GIT_WORK_TREE"] = clean
        try:
            check("GIT_DIR cannot redirect probes",
                  genie.clone_delete_blockers(env_victim), False, "uncommitted")
        finally:
            os.environ.pop("GIT_DIR", None)
            os.environ.pop("GIT_WORK_TREE", None)

        # 15. a repo that hides its own untracked files must still block
        hidden = make_clone(root, "hidden-untracked", origin)
        git(hidden, "config", "status.showUntrackedFiles", "no")
        write(hidden, "only-copy.txt", "never committed anywhere\n")
        check("status.showUntrackedFiles=no",
              genie.clone_delete_blockers(hidden), False, "uncommitted")

        # 16. stash whose reflog was expired -> refs/stash still holds the work
        expired = make_clone(root, "stash-expired", origin)
        write(expired, "f.txt", "hello\nstashed\n")
        git(expired, "stash")
        logs = os.path.join(expired, ".git", "logs")
        shutil.rmtree(logs, ignore_errors=True)
        check("stash with expired reflog",
              genie.clone_delete_blockers(expired), False, "stash")

        # 17. skip-worktree hides a tracked file's local-only content
        masked = make_clone(root, "skip-worktree", origin)
        git(masked, "update-index", "--skip-worktree", "f.txt")
        write(masked, "f.txt", "local-only content\n")
        check("skip-worktree masked file",
              genie.clone_delete_blockers(masked), False, "skip-worktree")

        # 18. a submodule holding an unpushed commit
        sub_origin = os.path.join(root, "sub.git")
        sh("git", "init", "-q", "--bare", "-b", "main", sub_origin)
        sub_seed = make_clone(root, "sub-seed", sub_origin)
        write(sub_seed, "s.txt", "sub\n")
        git(sub_seed, "add", "-A")
        git(sub_seed, "commit", "-q", "-m", "init")
        git(sub_seed, "push", "-q", "-u", "origin", "main")
        parent = make_clone(root, "with-submodule", origin)
        sh("git", "-C", parent, "-c", "protocol.file.allow=always",
           "submodule", "-q", "add", sub_origin, "sub")
        git(parent, "commit", "-q", "-m", "add submodule")
        git(parent, "push", "-q")
        subdir = os.path.join(parent, "sub")
        sh("git", "-C", subdir, "config", "user.email", "t@example.com")
        sh("git", "-C", subdir, "config", "user.name", "t")
        write(subdir, "local.txt", "submodule work that exists only here\n")
        sh("git", "-C", subdir, "add", "-A")
        sh("git", "-C", subdir, "commit", "-q", "-m", "sub local")
        blockers = genie.clone_delete_blockers(parent)
        check("submodule holds local work", blockers, False)

        # 19. a linked worktree depends on this clone's object store
        wt_owner = make_clone(root, "worktree-owner", origin)
        sh("git", "-C", wt_owner, "worktree", "add", "-q",
           os.path.join(root, "linked-wt"), "-b", "wt-branch")
        check("linked worktree exists",
              genie.clone_delete_blockers(wt_owner), False, "worktree")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    print()
    if FAILURES:
        print("FAILED: %s" % ", ".join(FAILURES))
        return 1
    print("ALL 19 GATE CASES PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
