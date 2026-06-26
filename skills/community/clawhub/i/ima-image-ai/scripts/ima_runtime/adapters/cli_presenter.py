from __future__ import annotations

import json

from ima_runtime.shared.config import MODEL_PROFILE_BY_ID


def print_model_summary(model_params: dict) -> None:
    print("✅ Model found:")
    print(f"   name          = {model_params['model_name']}")
    print(f"   model_id      = {model_params['model_id']}")
    print(f"   model_version = {model_params['model_version']}   ← version_id from product list")
    print(f"   attribute_id  = {model_params['attribute_id']}")
    print(f"   credit        = {model_params['credit']} pts")
    print(f"   form_params   = {json.dumps(model_params['form_params'], ensure_ascii=False)}")
    profile = MODEL_PROFILE_BY_ID.get(model_params["model_id"])
    if profile:
        print(f"   recommendation = {profile['summary']}")
        for feature in profile.get("features", ()):
            print(f"   feature       = {feature}")
