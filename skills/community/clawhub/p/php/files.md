# Files, Streams, and CSV

## Read Without Buying the Whole File

| Instead of | Use | Memory |
|---|---|---|
| `file_get_contents($p)` | `fopen` + `fgets`/`fread` loop | One chunk |
| `file($p)` | `SplFileObject` with `READ_AHEAD \| SKIP_EMPTY` | One line |
| `explode("\n", $csv)` | `fgetcsv($fh)` in a loop | One row |
| Building an array then returning it | A generator that `yield`s each row | One row |

- `file_get_contents` on a 400 MB export needs 400 MB plus every copy the pipeline makes, inside a 128M `memory_limit` (`performance.md`).
- A generator makes the caller's code identical while the memory profile becomes flat:

```php
function rows(string $path): \Generator {
    $fh = fopen($path, 'rb');
    if ($fh === false) { throw new RuntimeException("cannot open {$path}"); }
    try { while (($row = fgetcsv($fh, 0, ',', '"', '')) !== false) { yield $row; } }
    finally { fclose($fh); }
}
```

## CSV

- `fgetcsv`'s fifth parameter is `escape`, and its historical default is a backslash, which is NOT part of the CSV convention: a field containing `C:\path\` gets mangled. Pass `''` explicitly, on both `fgetcsv` and `fputcsv`.
- A UTF-8 BOM at the start of the file becomes part of the FIRST header cell, so `$row['id']` misses while `$row["\u{FEFF}id"]` would hit. Strip it: read the first three bytes and discard them if they are `\xEF\xBB\xBF` (`strings.md`).
- Spreadsheet software often writes `\r\n` and sometimes CP1252. Detect the encoding at the source rather than guessing per row, and convert once with an explicit source charset.
- Excel opens a UTF-8 CSV as CP1252 unless the file starts with a BOM — the one place where writing a BOM is correct.
- A leading `=`, `+`, `-`, or `@` in a cell is executed as a formula by spreadsheet software. When exporting user-supplied text, prefix such cells with a single quote or wrap them — CSV injection is a real finding in security reviews (`security.md`).
- `fputcsv` handles quoting and escaping; hand-built `implode(',', $row)` breaks on the first comma in a value.

## Writing Safely

- Atomic replace: write to a temporary file IN THE SAME DIRECTORY, then `rename()`. `rename` is atomic within a filesystem; across filesystems it degrades to copy-and-delete and loses atomicity, which is why `sys_get_temp_dir()` is the wrong place for the temp file.

```php
$tmp = $path . '.' . bin2hex(random_bytes(6)) . '.tmp';
file_put_contents($tmp, $data, LOCK_EX);
chmod($tmp, 0644);            // rename does not change permissions
rename($tmp, $path);          // readers see old or new, never partial
```

- `file_put_contents($p, $d, LOCK_EX)` prevents concurrent WRITERS from interleaving; it does not stop a reader from seeing a half-written file. Only the rename dance does.
- `fopen` modes: `w` truncates the moment it opens, before you have written anything — a crash between the two leaves an empty file. `c+` opens for read/write without truncating, which is what you want when you also need to `flock` and then truncate deliberately. `x` fails if the file exists, which is the race-free create.
- `a` (append) with writes under the OS pipe/write atomicity limit is effectively atomic on local filesystems — the reason concurrent log appends usually work.
- `flock` is advisory and unreliable over NFS. Cross-host mutual exclusion needs a real lock service (`concurrency.md`).

## Paths, Permissions, and Caching

- PHP caches `stat` results and `realpath` lookups. In a long-running process, a file created or renamed by someone else can stay invisible: `clearstatcache(true, $path)` after an external change (`cli.md`).
- `realpath()` returns `false` for a path that does not exist, which makes it useless for validating a path you are about to create — validate the parent directory instead.
- Containment against traversal: `realpath` the base, `realpath` the candidate, and require the candidate to start with the base PLUS a separator (`security.md`).
- `mkdir($p, 0775, true)` is affected by `umask`, so the created directory may have fewer bits than requested; `chmod` afterward when the exact mode matters. Recursive `mkdir` also races with a concurrent creator — check `is_dir()` after a failure rather than trusting the boolean.
- The FPM user owns the file a web request creates; a CLI job running as a different user then cannot overwrite it. One user for both, or a shared group with `g+w` and the setgid bit on the directory.
- `unlink()` on an open file handle succeeds on Linux (the data lives until the last handle closes) and fails on Windows. Cross-platform tools close first.

## Temporary Files

- `tmpfile()` returns a handle to a file deleted automatically when it closes — the safest scratch space.
- `tempnam(sys_get_temp_dir(), 'imp_')` creates the file atomically and returns its path; you own the cleanup, so wrap it in `try/finally`.
- Never construct a temp path by hand from a predictable name in `/tmp`: another process (or user) can win the race and plant a symlink.
- `php://temp` is a stream that lives in memory up to about 2 MB and then spills to disk; `php://memory` never spills. `php://temp/maxmemory:5242880` sets the threshold. Both are ideal for building a response body of unknown size without a real file (`http.md`).

## Streams and Wrappers

- Stream contexts carry timeouts and headers for `fopen`-family calls: without one, a remote read uses `default_socket_timeout` (60 seconds) and can occupy an FPM worker for a full minute (`http.md`).
- `stream_copy_to_stream($in, $out)` moves data between handles without materializing it in PHP memory — the correct way to pipe an upload to storage or a download to output.
- `stream_filter_append($fh, 'zlib.deflate')` compresses on the fly; the `convert.iconv.*` filter transcodes while streaming, which beats reading and converting the whole file.
- Custom wrappers via `stream_wrapper_register` are how libraries expose remote storage as a path. Beware the inverse: `allow_url_fopen` means any function taking a path can be pointed at a remote URL by user input (`security.md`).

## Traversal and Listing

- `glob()` does not match dotfiles by default, returns `false` on error (another `!== false` site), and has an implementation-defined limit on very large directories.
- Directory trees: `new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS))` — lazy, so a million-file tree does not become a million-element array.
- Sorting a directory listing is your job; the filesystem's order is not alphabetical and is not stable across systems.
- `SplFileInfo::getSize()` and `filesize()` are stat-cached; on a file being written, they lie until you clear the cache.

## Related

- Upload handling and download streaming: `http.md`, `security.md`
- Memory behavior of the streaming patterns: `performance.md`
- Encoding detection and BOMs: `strings.md`
