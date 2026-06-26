"""
PutBucketLifecycle for upload prefix (Aliyun OSS), aligned with LifecycleConfiguration:
prefix + Expiration.Days (last modified). Merges with existing rules by rule id.
"""

from __future__ import annotations

import oss2  # type: ignore[import-untyped]
from oss2.exceptions import NoSuchLifecycle  # type: ignore[import-untyped]
from oss2.models import BucketLifecycle, LifecycleExpiration, LifecycleRule  # type: ignore[import-untyped]


def _object_prefix(upload_dir: str) -> str:
    p = upload_dir.strip().strip("/")
    if not p:
        p = "upload"
    return p + "/"


def sync_upload_prefix_lifecycle(
    *,
    access_key_id: str,
    access_key_secret: str,
    endpoint: str,
    bucket_name: str,
    upload_dir: str,
    expire_days: int,
    rule_id: str,
) -> str:
    """
    GET lifecycle, replace rule with same id, PUT merged rules.
    Returns a short status line for logging.
    """
    if expire_days <= 0:
        raise ValueError("expire_days must be positive")
    rid = (rule_id or "").strip() or "keplerjai-oss-upload-expire"
    prefix = _object_prefix(upload_dir)

    ep = endpoint if endpoint.startswith("http") else f"https://{endpoint}"
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, ep, bucket_name)

    try:
        existing = bucket.get_bucket_lifecycle()
        rules = list(existing.rules)
    except NoSuchLifecycle:
        rules = []

    new_rule = LifecycleRule(
        rid,
        prefix,
        status=LifecycleRule.ENABLED,
        expiration=LifecycleExpiration(days=expire_days),
    )
    rules = [r for r in rules if getattr(r, "id", None) != rid]
    rules.append(new_rule)
    bucket.put_bucket_lifecycle(BucketLifecycle(rules))

    return (
        f"put_bucket_lifecycle ok bucket={bucket_name} rule_id={rid} "
        f"prefix={prefix!r} expiration_days={expire_days}"
    )
