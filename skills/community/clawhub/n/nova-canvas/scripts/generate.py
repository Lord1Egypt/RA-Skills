#!/usr/bin/env python3
"""Generate images using Amazon Nova Canvas via AWS Bedrock. Supports multiple AWS auth methods."""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error


def invoke_via_bearer_token(args, body):
    """Call Bedrock invoke-model using Bearer Token (AWS_BEARER_TOKEN_BEDROCK)."""
    token = os.environ.get("AWS_BEARER_TOKEN_BEDROCK", "")
    region = args.region

    url = f"https://bedrock-runtime.{region}.amazonaws.com/model/amazon.nova-canvas-v1%3A0/invoke"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    req = urllib.request.Request(url, data=body.encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        print(f"Error: Bedrock API {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)


def invoke_via_boto3(args, body):
    """Call Bedrock invoke-model using boto3 (standard AWS credential chain)."""
    try:
        import boto3
    except ImportError:
        print("Error: boto3 not installed. Run: pip install boto3", file=sys.stderr)
        sys.exit(1)

    kwargs = {"region_name": args.region}

    # Priority 1: Explicit keys
    if args.access_key and args.secret_key:
        kwargs["aws_access_key_id"] = args.access_key
        kwargs["aws_secret_access_key"] = args.secret_key
        if args.session_token:
            kwargs["aws_session_token"] = args.session_token
        print("  Auth: explicit keys")
        client = boto3.client("bedrock-runtime", **kwargs)
    # Priority 2: Named profile
    elif args.profile:
        session = boto3.Session(profile_name=args.profile, region_name=args.region)
        print(f"  Auth: profile ({args.profile})")
        client = session.client("bedrock-runtime")
    # Priority 3: Auto (env vars → credentials file → instance role → SSO)
    else:
        print("  Auth: boto3 auto-detect")
        client = boto3.client("bedrock-runtime", **kwargs)

    response = client.invoke_model(modelId="amazon.nova-canvas-v1:0", body=body)
    return json.loads(response["body"].read())


def detect_auth_method(args):
    """Determine which auth method to use."""
    # Explicit keys always win
    if args.access_key and args.secret_key:
        return "boto3"
    # Explicit profile
    if args.profile:
        return "boto3"
    # Bearer token
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
        return "bearer"
    # Check boto3 credentials
    try:
        import boto3
        session = boto3.Session(region_name=args.region)
        creds = session.get_credentials()
        if creds:
            return "boto3"
    except Exception:
        pass
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate images with Amazon Nova Canvas (AWS Bedrock)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
AWS auth methods (auto-detected):
  AWS_BEARER_TOKEN_BEDROCK      Bearer token (OpenClaw managed)
  --access-key + --secret-key   Direct IAM credentials
  --profile / AWS_PROFILE       Named profile (~/.aws/credentials)
  AWS_ACCESS_KEY_ID env var     Environment variables
  ~/.aws/credentials            Shared credentials file
  IAM instance role             EC2/ECS/Lambda
  AWS SSO                       aws sso login
""")
    # Image params
    parser.add_argument("prompt", help="Text description of the image")
    parser.add_argument("-o", "--output", default="output.png", help="Output path (default: output.png)")
    parser.add_argument("-W", "--width", type=int, default=1024, help="Width 512-4096, ÷64 (default: 1024)")
    parser.add_argument("-H", "--height", type=int, default=1024, help="Height 512-4096, ÷64 (default: 1024)")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of images 1-5 (default: 1)")
    parser.add_argument("-q", "--quality", choices=["standard", "premium"], default="standard")
    parser.add_argument("-s", "--seed", type=int, default=None, help="Seed (0-858993459)")
    parser.add_argument("--negative", help="Negative prompt")
    parser.add_argument("--cfg", type=float, default=8.0, help="CFG scale 1.1-10.0 (default: 8.0)")

    # AWS auth params
    parser.add_argument("--region", default="us-east-1", help="AWS region (default: us-east-1, Nova Canvas availability)")
    parser.add_argument("--profile", default=None, help="AWS named profile")
    parser.add_argument("--access-key", default=None, help="AWS Access Key ID")
    parser.add_argument("--secret-key", default=None, help="AWS Secret Access Key")
    parser.add_argument("--session-token", default=None, help="AWS Session Token")
    parser.add_argument("--bearer-token", default=None, help="Bearer token (overrides AWS_BEARER_TOKEN_BEDROCK)")

    args = parser.parse_args()

    # Allow --bearer-token to override env
    if args.bearer_token:
        os.environ["AWS_BEARER_TOKEN_BEDROCK"] = args.bearer_token

    # Validate dimensions
    for name, val in [("width", args.width), ("height", args.height)]:
        if val < 512 or val > 4096:
            print(f"Error: {name} must be 512-4096, got {val}", file=sys.stderr)
            sys.exit(1)
        if val % 64 != 0:
            print(f"Error: {name} must be divisible by 64, got {val}", file=sys.stderr)
            sys.exit(1)

    # Detect auth
    method = detect_auth_method(args)
    if not method:
        print("Error: No AWS credentials found. Options:", file=sys.stderr)
        print("  1. AWS_BEARER_TOKEN_BEDROCK env var (OpenClaw managed)", file=sys.stderr)
        print("  2. AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY env vars", file=sys.stderr)
        print("  3. ~/.aws/credentials file", file=sys.stderr)
        print("  4. --profile <name>", file=sys.stderr)
        print("  5. --access-key + --secret-key", file=sys.stderr)
        print("  6. --bearer-token <token>", file=sys.stderr)
        print("  7. IAM instance role (EC2/ECS/Lambda)", file=sys.stderr)
        print("  8. AWS SSO (aws sso login)", file=sys.stderr)
        sys.exit(1)

    # Build request body
    text_params = {"text": args.prompt}
    if args.negative:
        text_params["negativeText"] = args.negative

    img_cfg = {
        "numberOfImages": args.count,
        "height": args.height,
        "width": args.width,
        "quality": args.quality,
        "cfgScale": args.cfg,
    }
    if args.seed is not None:
        img_cfg["seed"] = args.seed

    body = json.dumps({
        "taskType": "TEXT_IMAGE",
        "textToImageParams": text_params,
        "imageGenerationConfig": img_cfg,
    })

    print(f"Generating {args.count} image(s) at {args.width}x{args.height} ({args.quality})...")

    # Invoke
    try:
        if method == "bearer":
            print("  Auth: Bearer token")
            result = invoke_via_bearer_token(args, body)
        else:
            result = invoke_via_boto3(args, body)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if "images" not in result or not result["images"]:
        print(f"Error: No images returned. {json.dumps(result, indent=2)}", file=sys.stderr)
        sys.exit(1)

    # Save
    output_dir = os.path.dirname(args.output) or "."
    base_name = os.path.splitext(os.path.basename(args.output))[0]
    ext = os.path.splitext(args.output)[1] or ".png"
    os.makedirs(output_dir, exist_ok=True)

    paths = []
    for i, img_b64 in enumerate(result["images"]):
        path = args.output if args.count == 1 else os.path.join(output_dir, f"{base_name}_{i+1}{ext}")
        with open(path, "wb") as f:
            f.write(base64.b64decode(img_b64))
        size_kb = os.path.getsize(path) / 1024
        print(f"  [{i+1}/{len(result['images'])}] {path} ({size_kb:.0f} KB)")
        paths.append(path)

    print(f"Done. {len(paths)} image(s) saved.")
    return paths


if __name__ == "__main__":
    main()
