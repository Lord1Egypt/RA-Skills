# Verification Method

This skill provides two independent ways to collect OBS aggregate statistics:
the KooCLI obsutil-backed command (primary) and the `huaweicloudsdkobs` Python
SDK (fallback).

## Offline Unit Tests

Run the bundled test suite (no credentials, no network — the hcloud subprocess
and the SDK are mocked):

```bash
python3 -m unittest discover -s tests -v
```

## Manual Verification Steps

1. **Prerequisite check** — confirm hcloud / obsutil are available:

   ```bash
   hcloud version
   hcloud OBS ls -limit=1 -e=obs.cn-north-4.myhuaweicloud.com
   ```

   If the second command returns `Please set ak, sk and endpoint in the
   configuration file!`, obsutil credentials are not configured.

2. **Single bucket, all objects**:

   ```bash
   python3 scripts/collect_obs_stats.py --bucket <bucket_name>
   ```

   Expected: a table with bucket/object counts, total capacity, storage-class
   distribution and region distribution.

3. **Prefix scope**:

   ```bash
   python3 scripts/collect_obs_stats.py --bucket <bucket_name> --prefix <prefix>
   ```

   Expected: object count and capacity reflect only the prefix.

4. **JSON output** — verify the structured object:

   ```bash
   python3 scripts/collect_obs_stats.py --bucket <bucket_name> --json | python3 -m json.tool
   ```

   Expected: `summary.bucket_count`, `summary.object_count`,
   `summary.total_size_bytes`, `storage_class_distribution`,
   `region_distribution`, `buckets`, `truncated`.

5. **Markdown output**:

   ```bash
   python3 scripts/collect_obs_stats.py --bucket <bucket_name> --output md
   ```

6. **SDK fallback** — verify the SDK path returns the same shape:

   ```bash
   python3 scripts/collect_obs_stats.py --bucket <bucket_name> --executor sdk
   ```

7. **Empty scope** — an empty bucket returns a zeroed report and exit code 0.

8. **Nonexistent bucket** — the script exits non-zero and prints a clear
   Chinese hint on stderr (e.g. `NoSuchBucket`).

9. **Missing credentials** — run the SDK path without AK/SK env vars:

   ```bash
   env -u HW_ACCESS_KEY -u HUAWEI_ACCESS_KEY -u HUAWEICLOUD_SDK_AK \
       python3 scripts/collect_obs_stats.py --bucket <bucket_name> --executor sdk
   ```

   Expected: exit code 1, stderr contains the Chinese credential hint.

10. **Write intent rejected**:

    ```bash
    python3 scripts/collect_obs_stats.py --operation CreateBucket
    ```

    Expected: exit code 1, stderr contains `检测到写操作意图`.

## Pass Criteria

- All three output modes render the same aggregated numbers.
- CLI and SDK paths agree on the totals for the same scope.
- No create/update/delete operation is ever performed.
- Error paths (nonexistent bucket, missing credentials, write intent) exit
  non-zero with a clear Chinese hint on stderr.