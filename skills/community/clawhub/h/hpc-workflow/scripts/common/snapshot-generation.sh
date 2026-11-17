# Immutable generations. Only CURRENT is the commit point; legacy paths are views.
generation_metadata() {
    python3 - "$@" <<'PY'
import hashlib, json, os, sys, time
from pathlib import Path
action, directory = sys.argv[1:3]
root = Path(directory)
def sync_directory(path):
    fd = os.open(str(path), os.O_RDONLY | os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)
if action == 'dirsync':
    sync_directory(root); sys.exit(0)
def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()
def verify_record(candidate, record):
    members = sorted([candidate / 'full.tar.zst', candidate / 'full.tar.zst.inc/snapshot.snar'] +
                     list((candidate / 'full.tar.zst.inc').glob('*.tar.zst')))
    assert record['schema_version'] == 1
    assert set(record['files']) == {str(p.relative_to(candidate)) for p in members}, 'generation file set changed'
    for p in members:
        assert not p.is_symlink(), 'unexpected symlink in generation'
        assert digest(p) == record['files'][str(p.relative_to(candidate))], str(p) + ': SHA256 mismatch'
files = sorted([root / 'full.tar.zst', root / 'full.tar.zst.inc/snapshot.snar'] +
               list((root / 'full.tar.zst.inc').glob('*.tar.zst')))
if action == 'identity':
    with (root / 'manifest.json').open() as stream: print(json.load(stream)['baseline_identity'])
    sys.exit(0)
if action == 'seal':
    previous = Path(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] else None
    inherited = {}
    previous_record = {}
    if previous:
        with (previous / 'manifest.json').open() as stream: previous_record = json.load(stream)
        inherited = previous_record['files']
    def sealed_digest(p):
        name = str(p.relative_to(root))
        # The previous generation was verified under the archive lock; only
        # unchanged pack inodes can reuse its digest. Baselines are never linked.
        if previous and name in inherited and (previous / name).exists() and os.path.samefile(p, previous / name):
            return inherited[name]
        value = digest(p)
        with p.open('rb') as stream: os.fsync(stream.fileno())
        return value
    record = dict(schema_version=1, committed_ns=int(time.time()*1e9),
                  baseline_identity=sys.argv[3],
                  files={str(p.relative_to(root)): sealed_digest(p) for p in files})
    family = root.name.replace('stage-', 'gen-', 1)
    if previous and os.path.samefile(root / 'full.tar.zst', previous / 'full.tar.zst'):
        family = previous_record.get('full_generation', previous.name)
    record['full_generation'] = family
    with (root / 'manifest.json').open('w') as stream:
        json.dump(record, stream, sort_keys=True)
        stream.flush(); os.fsync(stream.fileno())
    sync_directory(root / 'full.tar.zst.inc')
    sync_directory(root)
elif action == 'retention':
    keep, families_keep = map(int, sys.argv[3:5])
    families = set()
    count = 0
    for p in sorted(root.glob('gen-*'), reverse=True):
        if (p / 'invalid').exists() or not (p / 'manifest.json').exists(): continue
        with (p / 'manifest.json').open() as stream: record = json.load(stream)
        family = record.get('full_generation', p.name)
        keep_family = family not in families and len(families) < families_keep
        if keep_family and str(p) != sys.argv[5]:
            try:
                verify_record(p, record)
            except (OSError, ValueError, AssertionError) as error:
                (p / 'invalid').touch()
                print('SNAPSHOT_INVALID preserved={} error={}'.format(p, error), file=sys.stderr)
                continue
        families.add(family)
        count += 1
        if count > keep and not keep_family: print(p)
else:
    with (root / 'manifest.json').open() as stream:
        record = json.load(stream)
    verify_record(root, record)
    if action == 'identity':
        print(record['baseline_identity'])
PY
}

generation_identity() {
    printf '%s:%s:%s\n' "$(hostname)" "${SLURM_JOB_ID:-standalone}" "$(local_base)"
}

generation_select() {
    local archive="$1" candidate current found=0
    current="$(readlink -f "$archive.current" 2>/dev/null || true)"
    # CURRENT first, then earlier commits; an incomplete stage has no manifest.
    while IFS= read -r candidate; do
        [[ -n "$candidate" && -f "$candidate/manifest.json" ]] || continue
        if generation_metadata verify "$candidate"; then
            [[ "$candidate" == "$current" ]] || echo "SNAPSHOT_FALLBACK generation=$candidate" >&2
            printf '%s\n' "$candidate"
            return 0
        fi
        echo "SNAPSHOT_INVALID preserved=$candidate" >&2
        touch "$candidate/invalid"
        found=1
    done < <({ [[ -z "$current" ]] || printf '%s\n' "$current";
               find "$archive.generations" -mindepth 1 -maxdepth 1 -type d -name 'gen-*' 2>/dev/null | sort -r; })
    if [[ -L "$archive.current" || "$found" == 1 ]]; then
        die "no verified generation remains; preserving evidence"
    fi
    return 2
}

generation_clone() {
    local source="$1" destination="$2"
    # Large packs share inodes, but the tar baseline must be independently mutable.
    cp -al "$source/full.tar.zst" "$destination/full.tar.zst"
    cp -al "$source/full.tar.zst.inc" "$destination/full.tar.zst.inc"
    rm -f "$destination/full.tar.zst.inc/snapshot.snar"
    cp "$source/full.tar.zst.inc/snapshot.snar" "$destination/full.tar.zst.inc/snapshot.snar"
}

generation_publish() {
    local archive="$1" stage="$2" target tmp candidate keep families_keep
    generation_metadata seal "$stage" "$(generation_identity)" "${3:-}"
    [[ "${@PREFIX@_LOCAL_SNAPSHOT_TEST_FAILPOINT:-}" != before_commit ]] || die 'test interruption before commit'
    target="$(dirname "$stage")/gen-${stage##*/stage-}"
    mv "$stage" "$target"
    generation_metadata dirsync "$archive.generations"
    tmp="$archive.current.tmp.$$"
    ln -s "$target" "$tmp"
    mv -Tf "$tmp" "$archive.current"
    generation_metadata dirsync "$(dirname "$archive")"
    # Preserve the legacy chain during one-time migration; never delete it.
    if [[ ! -L "$archive" && -e "$archive" ]]; then mv "$archive" "$archive.legacy"; fi
    if [[ ! -L "$archive.inc" && -d "$archive.inc" ]]; then mv "$archive.inc" "$archive.legacy.inc"; fi
    ln -s "$archive.current/full.tar.zst" "$archive.view.$$"
    mv -Tf "$archive.view.$$" "$archive"
    ln -s "$archive.current/full.tar.zst.inc" "$archive.inc.view.$$"
    mv -Tf "$archive.inc.view.$$" "$archive.inc"
    # Retention touches only owned, complete, verified generations. Invalid ones
    # are evidence and remain untouched; hardlinks avoid duplicating full packs.
    keep="${@PREFIX@_LOCAL_SNAPSHOT_GENERATIONS_KEEP:-3}"
    families_keep="${@PREFIX@_LOCAL_SNAPSHOT_FULL_FAMILIES_KEEP:-2}"
    [[ "$keep" =~ ^[0-9]+$ && "$keep" -ge 2 ]] || die 'GENERATIONS_KEEP must be at least 2'
    while IFS= read -r candidate; do
        [[ "$candidate" != "$target" ]] || continue
        if generation_metadata verify "$candidate"; then rm -rf -- "$candidate"
        else touch "$candidate/invalid"; fi
    done < <(generation_metadata retention "$archive.generations" "$keep" "$families_keep" "$target")
    printf 'SNAPSHOT_COMMITTED generation=%s\n' "$target" >&2
}

transaction_cmd() {
    local action="$1" archive source='' stage selected_rc identity
    # Validate local storage before cloning or verifying network snapshots.
    # Explicit propagation also protects calls made from Bash conditionals.
    if [[ "$action" != verify ]]; then
        ensure_base >/dev/null || return $?
    fi
    archive="$(archive_path "${2:-}")"
    operation="${action}_cmd"
    local keep="${@PREFIX@_LOCAL_SNAPSHOT_GENERATIONS_KEEP:-3}"
    [[ "$keep" =~ ^[0-9]+$ && "$keep" -ge 2 ]] || die 'GENERATIONS_KEEP must be at least 2'
    local families_keep="${@PREFIX@_LOCAL_SNAPSHOT_FULL_FAMILIES_KEEP:-2}"
    [[ "$families_keep" =~ ^[0-9]+$ && "$families_keep" -ge 2 ]] || die 'FULL_FAMILIES_KEEP must be at least 2'
    mkdir -p "$archive.generations"
    if source="$(generation_select "$archive")"; then :
    else
        selected_rc=$?
        [[ "$selected_rc" == 2 ]] || return "$selected_rc"
        source=''
    fi
    if [[ "$action" == verify ]]; then
        if [[ -n "$source" ]]; then printf 'SNAPSHOT_VERIFIED generation=%s\n' "$source"; return; fi
        [[ -f "$archive" ]] || { echo SNAPSHOT_EMPTY; return; }
        verify_pack "$archive"
        local pack
        while IFS= read -r pack; do verify_pack "$pack"; done < <(find "$archive.inc" -maxdepth 1 -name '*.tar.zst' -type f 2>/dev/null | sort)
        echo SNAPSHOT_VERIFIED_LEGACY
        return
    fi
    if [[ "$action" == restore && -z "$source" && ! -f "$archive" ]]; then
        ensure_base || return $?; echo SNAPSHOT_EMPTY; return
    fi
    stage="$(mktemp -d "$archive.generations/stage-$(date +%Y%m%dT%H%M%S%N)-XXXXXXXX")"
    if [[ "$action" != save && "$action" != compact ]]; then
        if [[ -n "$source" ]]; then
            generation_clone "$source" "$stage"
            identity="$(generation_metadata identity "$source")"
            if [[ "$action" == incsave && "$identity" != "$(generation_identity)" ]]; then
                die 'baseline belongs to another allocation; restore before saving'
            fi
        elif [[ -f "$archive" ]]; then
            cp -al "$archive" "$stage/full.tar.zst"
            # Dereference only the top-level compatibility view, never tree links.
            [[ ! -d "$archive.inc" ]] || cp -a "$archive.inc/." "$stage/full.tar.zst.inc/"
        fi
    fi
    case "$action" in
        restore) restore_cmd "$stage/full.tar.zst" ;;
        rebaseline) rebaseline_cmd "$stage/full.tar.zst" ;;
        save|compact) save_cmd "$stage/full.tar.zst" ;;
        incsave) incsave_cmd "$stage/full.tar.zst" ;;
        *) die "unknown transaction: $action" ;;
    esac
    generation_publish "$archive" "$stage" "$source"
    echo "$archive"
}
