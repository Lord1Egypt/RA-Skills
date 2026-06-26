#!/usr/bin/env python3
"""
OCR Benchmark v2.0.0 — Multi-model OCR accuracy comparison.
Runs OCR on images using multiple providers, saves JSON results,
and scores each model against a human-verified ground truth.

Usage:
  python3 run_benchmark.py --images img1.jpg img2.jpg --output-dir ./results
  python3 run_benchmark.py --images img1.jpg --models opus sonnet gemini3pro
  python3 run_benchmark.py --images img1.jpg --ground-truth gt.json --output-dir ./results
  python3 run_benchmark.py --score-only --output-dir ./results --ground-truth gt.json
  python3 run_benchmark.py --images img1.jpg --auto-skip   # skip models missing env vars

Environment variables:
  AWS_REGION           — Bedrock region (default: us-west-2)
  GOOGLE_API_KEY       — Google AI Studio API key (for Gemini models)
  PADDLEOCR_TOKEN      — PaddleOCR API token (optional)
  PADDLEOCR_ENDPOINT   — PaddleOCR endpoint URL (optional; if unset, PaddleOCR is skipped)
"""

import argparse, base64, json, os, sys, time, mimetypes

VERSION = "2.0.0"

# ──────────────────── Model Registry ────────────────────
MODELS = {
    'opus': {
        'provider': 'bedrock',
        'model_id': 'global.anthropic.claude-opus-4-6-v1',
        'label': 'Claude Opus 4.6',
        'input_price': 15.0,    # per 1M tokens
        'output_price': 75.0,
        'required_env': [],     # uses AWS_DEFAULT_REGION/credentials
    },
    'sonnet': {
        'provider': 'bedrock',
        'model_id': 'global.anthropic.claude-sonnet-4-6',
        'label': 'Claude Sonnet 4.6',
        'input_price': 3.0,
        'output_price': 15.0,
        'required_env': [],
    },
    'haiku': {
        'provider': 'bedrock',
        'model_id': 'us.anthropic.claude-haiku-4-5-20251001-v1:0',
        'label': 'Claude Haiku 4.5',
        'input_price': 0.80,
        'output_price': 4.0,
        'required_env': [],
    },
    'gemini3pro': {
        'provider': 'gemini',
        'model_id': 'gemini-3.1-pro-preview',
        'label': 'Gemini 3.1 Pro',
        'input_price': 2.0,
        'output_price': 12.0,
        'required_env': ['GOOGLE_API_KEY'],
    },
    'gemini3flash': {
        'provider': 'gemini',
        'model_id': 'gemini-3.1-flash-lite-preview',
        'label': 'Gemini 3.1 Flash-Lite',
        'input_price': 0.25,
        'output_price': 1.50,
        'required_env': ['GOOGLE_API_KEY'],
    },
    'paddleocr': {
        'provider': 'paddleocr',
        'model_id': 'paddleocr',
        'label': 'PaddleOCR',
        'input_price': 0,
        'output_price': 0,
        'required_env': ['PADDLEOCR_ENDPOINT'],
    },
}

DEFAULT_MODELS = ['opus', 'sonnet', 'haiku', 'gemini3pro', 'gemini3flash', 'paddleocr']

OCR_PROMPT = """Extract ALL text visible in this image. Return a JSON object with:
{
  "text_extracted": ["line1", "line2", ...],
  "brand": "...",
  "product_name": "...",
  "net_weight": "...",
  "ingredients": ["..."],
  "other_fields": {}
}
Include every piece of text: product names, weights, ingredients, disclaimers, fine print.
For Chinese text, preserve original characters exactly. Do not translate.
Return each distinct line of text as a separate element in text_extracted."""

# ──────────────────── Environment Check ────────────────────
def check_model_env(model_key):
    """Returns (ok: bool, missing: list[str])."""
    cfg = MODELS[model_key]
    missing = [v for v in cfg.get('required_env', []) if not os.environ.get(v)]
    # Bedrock: check boto3 importability and AWS credentials indirectly
    if cfg['provider'] == 'bedrock':
        try:
            import boto3  # noqa: F401
        except ImportError:
            missing.append('boto3 (pip install boto3)')
    elif cfg['provider'] == 'gemini':
        try:
            from google import genai  # noqa: F401
        except ImportError:
            missing.append('google-genai (pip install google-genai)')
    elif cfg['provider'] == 'paddleocr':
        try:
            import requests  # noqa: F401
        except ImportError:
            missing.append('requests (pip install requests)')
    return (len(missing) == 0), missing

# ──────────────────── Bedrock Provider ────────────────────
def ocr_bedrock(image_path, model_id):
    import boto3
    region = os.environ.get('AWS_REGION', 'us-west-2')
    client = boto3.client('bedrock-runtime', region_name=region)

    mime = mimetypes.guess_type(image_path)[0] or 'image/jpeg'
    fmt = mime.split('/')[-1]
    if fmt == 'jpg':
        fmt = 'jpeg'

    with open(image_path, 'rb') as f:
        img_bytes = f.read()

    t0 = time.time()
    resp = client.converse(
        modelId=model_id,
        messages=[{
            'role': 'user',
            'content': [
                {'image': {'format': fmt, 'source': {'bytes': img_bytes}}},
                {'text': OCR_PROMPT},
            ]
        }],
        inferenceConfig={'maxTokens': 8192, 'temperature': 0.0},
    )
    latency = round(time.time() - t0, 2)

    text = resp['output']['message']['content'][0]['text']
    usage = resp.get('usage', {})
    return text, latency, usage.get('inputTokens', 0), usage.get('outputTokens', 0)

# ──────────────────── Gemini Provider ────────────────────
def ocr_gemini(image_path, model_id):
    from google import genai

    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        raise RuntimeError('GOOGLE_API_KEY not set')

    client = genai.Client(api_key=api_key)
    mime = mimetypes.guess_type(image_path)[0] or 'image/jpeg'

    with open(image_path, 'rb') as f:
        img_bytes = f.read()

    img_part = genai.types.Part.from_bytes(data=img_bytes, mime_type=mime)
    text_part = genai.types.Part.from_text(text=OCR_PROMPT)

    t0 = time.time()
    resp = client.models.generate_content(
        model=model_id,
        contents=genai.types.Content(parts=[img_part, text_part]),
        config=genai.types.GenerateContentConfig(temperature=0.0, max_output_tokens=8192),
    )
    latency = round(time.time() - t0, 2)

    text = resp.text
    usage = resp.usage_metadata
    return text, latency, getattr(usage, 'prompt_token_count', 0), getattr(usage, 'candidates_token_count', 0)

# ──────────────────── PaddleOCR Provider ────────────────────
def ocr_paddleocr(image_path, model_id=None):
    import requests

    endpoint = os.environ.get('PADDLEOCR_ENDPOINT', '')
    if not endpoint:
        raise RuntimeError('PADDLEOCR_ENDPOINT not set — PaddleOCR is optional, set env var to enable')
    token = os.environ.get('PADDLEOCR_TOKEN', '')

    with open(image_path, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()

    t0 = time.time()
    resp = requests.post(
        endpoint,
        json={'image': img_b64},
        headers={'Authorization': f'token {token}'} if token else {},
        timeout=30,
    )
    latency = round(time.time() - t0, 2)
    resp.raise_for_status()

    result = resp.json()
    texts = []
    for item in result.get('result', []):
        if isinstance(item, dict) and 'text' in item:
            texts.append(item['text'])
        elif isinstance(item, list):
            for sub in item:
                if isinstance(sub, dict) and 'text' in sub:
                    texts.append(sub['text'])

    return json.dumps({'text_extracted': texts}, ensure_ascii=False), latency, 0, 0

# ──────────────────── Dispatcher ────────────────────
def run_ocr(image_path, model_key):
    cfg = MODELS[model_key]
    provider = cfg['provider']

    if provider == 'bedrock':
        text, latency, in_tok, out_tok = ocr_bedrock(image_path, cfg['model_id'])
    elif provider == 'gemini':
        text, latency, in_tok, out_tok = ocr_gemini(image_path, cfg['model_id'])
    elif provider == 'paddleocr':
        text, latency, in_tok, out_tok = ocr_paddleocr(image_path)
    else:
        raise ValueError(f'Unknown provider: {provider}')

    # Parse JSON from response
    try:
        cleaned = text.strip()
        if cleaned.startswith('```'):
            lines = cleaned.split('\n')
            # strip first line (```json or ```) and last ```
            cleaned = '\n'.join(lines[1:])
        if cleaned.endswith('```'):
            cleaned = cleaned[:cleaned.rfind('```')]
        data = json.loads(cleaned.strip())
    except json.JSONDecodeError:
        data = {'text_extracted': [text], 'raw_response': True}

    data['source'] = image_path
    data['model'] = cfg['label']
    data['model_key'] = model_key
    data['latency_seconds'] = latency
    data['input_tokens'] = in_tok
    data['output_tokens'] = out_tok

    return data

# ──────────────────── Fuzzy Scoring (stdlib only) ────────────────────

def levenshtein(s1, s2):
    """Compute Levenshtein edit distance between two strings (stdlib only)."""
    if s1 == s2:
        return 0
    len1, len2 = len(s1), len(s2)
    if len1 == 0:
        return len2
    if len2 == 0:
        return len1
    # Use two rows for memory efficiency
    prev = list(range(len2 + 1))
    curr = [0] * (len2 + 1)
    for i in range(1, len1 + 1):
        curr[0] = i
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            curr[j] = min(
                curr[j - 1] + 1,       # insertion
                prev[j] + 1,           # deletion
                prev[j - 1] + cost,    # substitution
            )
        prev, curr = curr, prev
    return prev[len2]


def classify_match(gt_text, candidate, threshold_close=0.20, threshold_partial=0.50):
    """
    Compare gt_text and candidate, return (match_type, edit_distance, ratio).

    Match types:
      EXACT   — identical after normalization (score 1.0)
      CLOSE   — edit_dist / max_len < threshold_close (score 0.8)
                → punctuation/apostrophe diffs, minor formatting
      PARTIAL — edit_dist / max_len <= threshold_partial (score 0.5)
                → real character errors but substantial overlap
      MISS    — edit_dist / max_len > threshold_partial (score 0.0)

    Normalization: strips whitespace, apostrophes/quotes, common CJK/ASCII
    punctuation, then lowercases. This means "Sam's" == "Sams" after norm
    (apostrophe stripped), so they score EXACT — which is correct for OCR
    evaluation since apostrophe omission is a minor formatting difference.
    """
    import re
    def norm(t):
        t = t.strip().lower()
        # Normalize apostrophes/smart quotes → remove
        t = re.sub(r"[''`´'']", "", t)
        # Strip common punctuation that shouldn't affect accuracy scoring
        t = re.sub(r'[\s\*✓,，、:：()（）\+\-—–\[\]【】《》""\"\']+', '', t)
        return t

    n_gt = norm(gt_text)
    n_cand = norm(candidate)

    if n_gt == n_cand:
        return 'EXACT', 0, 1.0

    dist = levenshtein(n_gt, n_cand)
    max_len = max(len(n_gt), len(n_cand), 1)
    ratio = dist / max_len

    if ratio < threshold_close:
        return 'CLOSE', dist, round(1.0 - ratio, 3)
    elif ratio <= threshold_partial:
        return 'PARTIAL', dist, round(1.0 - ratio, 3)
    else:
        return 'MISS', dist, round(1.0 - ratio, 3)


MATCH_SCORES = {'EXACT': 1.0, 'CLOSE': 0.8, 'PARTIAL': 0.5, 'MISS': 0.0}


def best_match_for_gt_line(gt_line, candidate_lines):
    """
    Find the best matching candidate for a single ground truth line.
    Returns (match_type, best_candidate, edit_dist, similarity_ratio).
    """
    best = ('MISS', '', 0, 0.0)
    best_score = -1.0

    for cand in candidate_lines:
        mtype, dist, ratio = classify_match(gt_line, cand)
        score = MATCH_SCORES[mtype]
        # Tie-break: prefer higher similarity ratio
        if score > best_score or (score == best_score and ratio > best[3]):
            best = (mtype, cand, dist, ratio)
            best_score = score

    return best


def find_extra_lines(gt_lines, model_lines, threshold_close=0.20):
    """
    Find model output lines that don't match any ground truth line.
    Returns list of (model_line, closest_gt, similarity_ratio).
    """
    import re
    def norm(t):
        t = t.strip().lower()
        t = re.sub(r"[''`´]", "", t)
        t = re.sub(r'[\s\*✓,，、:：()（）\+\-—–\[\]【】《》""\"\']+', '', t)
        return t

    extras = []
    for mline in model_lines:
        if not norm(mline):
            continue  # skip blank/whitespace-only lines
        best_match_type = 'MISS'
        closest_gt = ''
        best_ratio = 0.0
        for gt in gt_lines:
            mtype, dist, ratio = classify_match(gt, mline)
            if MATCH_SCORES[mtype] > MATCH_SCORES[best_match_type] or ratio > best_ratio:
                best_match_type = mtype
                closest_gt = gt
                best_ratio = ratio
        if best_match_type == 'MISS':
            extras.append({'line': mline, 'closest_gt': closest_gt, 'similarity': best_ratio})

    return extras


# ──────────────────── Scoring Engine ────────────────────
def score_results(results_dir, ground_truth_path=None, verbose=True):
    """
    Score all model results against ground truth with fuzzy line-level matching.

    Returns a scores dict keyed by model_key, or None if no ground truth.
    """
    if not ground_truth_path or not os.path.exists(ground_truth_path):
        if verbose:
            print("No ground truth file provided, skipping scoring.")
        return None

    with open(ground_truth_path, 'r', encoding='utf-8') as f:
        gt = json.load(f)

    scores = {}

    for fname in sorted(os.listdir(results_dir)):
        if not fname.endswith('.json'):
            continue
        if fname in ('ground_truth.json', 'scores.json'):
            continue

        parts = fname[:-5].split('.')  # strip .json, split on .
        if len(parts) < 2:
            continue
        img_name = '.'.join(parts[:-1])   # everything before last segment
        model_key = parts[-1]

        if img_name not in gt:
            continue

        gt_lines = [l for l in gt[img_name] if l.strip()]
        with open(os.path.join(results_dir, fname), 'r', encoding='utf-8') as f:
            data = json.load(f)

        model_lines = data.get('text_extracted', [])
        model_lines = [l for l in model_lines if isinstance(l, str) and l.strip()]

        # Per-line matching
        line_results = []
        total_score = 0.0

        for gt_line in gt_lines:
            mtype, best_cand, dist, ratio = best_match_for_gt_line(gt_line, model_lines)
            line_score = MATCH_SCORES[mtype]
            total_score += line_score
            line_results.append({
                'gt': gt_line,
                'matched': best_cand,
                'type': mtype,
                'score': line_score,
                'edit_dist': dist,
                'similarity': ratio,
            })

        # Extra lines detection
        extra_lines = find_extra_lines(gt_lines, model_lines)

        img_pct = round(total_score / len(gt_lines) * 100, 1) if gt_lines else 0.0

        if model_key not in scores:
            scores[model_key] = {
                'total_score': 0.0,
                'total_items': 0,
                'images': {},
            }

        scores[model_key]['total_score'] += total_score
        scores[model_key]['total_items'] += len(gt_lines)
        scores[model_key]['images'][img_name] = {
            'score': total_score,
            'total': len(gt_lines),
            'pct': img_pct,
            'line_results': line_results,
            'extra_lines': extra_lines,
        }

    # Compute overall percentages
    for mk in scores:
        s = scores[mk]
        s['overall_pct'] = round(
            s['total_score'] / s['total_items'] * 100, 1
        ) if s['total_items'] > 0 else 0.0

    out = os.path.join(results_dir, 'scores.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)

    if verbose:
        print(f"Scores saved to {out}")

    return scores


# ──────────────────── Terminal Report ────────────────────
def print_terminal_report(scores, models_registry=None):
    """Print a human-readable table report to stdout."""
    if not scores:
        print("No scores to report.")
        return

    reg = models_registry or MODELS

    # ── Summary ranking table ──
    ranked = sorted(scores.items(), key=lambda x: -x[1]['overall_pct'])
    medals = ['🥇', '🥈', '🥉']

    print()
    print("=" * 72)
    print(f"  {'OCR BENCHMARK RESULTS':^68}")
    print("=" * 72)
    print(f"  {'#':<4} {'Model':<28} {'Score':>7}  {'Details'}")
    print("-" * 72)

    for i, (mk, s) in enumerate(ranked):
        medal = medals[i] if i < 3 else f'{i+1:2d}.'
        label = reg.get(mk, {}).get('label', mk)
        overall = s['overall_pct']

        # Build per-image mini summary
        img_parts = []
        for img, img_data in sorted(s['images'].items()):
            img_parts.append(f"{img}: {img_data['pct']:.0f}%")
        img_summary = ' | '.join(img_parts)

        print(f"  {medal:<4} {label:<28} {overall:>6.1f}%  {img_summary}")

    print("=" * 72)

    # ── Per-image per-model detail ──
    all_images = set()
    for s in scores.values():
        all_images.update(s['images'].keys())

    for img_name in sorted(all_images):
        print()
        print(f"  📄 {img_name}")
        print(f"  {'─' * 68}")

        for mk, s in ranked:
            if img_name not in s['images']:
                continue
            label = reg.get(mk, {}).get('label', mk)
            img_data = s['images'][img_name]
            line_results = img_data.get('line_results', [])
            extra_lines = img_data.get('extra_lines', [])

            print(f"  ┌─ {label} ({img_data['pct']:.1f}%)")

            for lr in line_results:
                icon = {'EXACT': '✅', 'CLOSE': '🟡', 'PARTIAL': '🟠', 'MISS': '❌'}[lr['type']]
                gt_disp = lr['gt'][:40]
                if lr['type'] == 'EXACT':
                    print(f"  │  {icon} EXACT   │ {gt_disp}")
                elif lr['type'] == 'MISS':
                    print(f"  │  {icon} MISS    │ GT: {gt_disp}")
                else:
                    matched_disp = lr['matched'][:40]
                    print(f"  │  {icon} {lr['type']:<7} │ GT: {gt_disp}")
                    print(f"  │           │ Got: {matched_disp}  [dist={lr['edit_dist']}]")

            if extra_lines:
                print(f"  │  ⚠️  EXTRA lines ({len(extra_lines)}):")
                for ex in extra_lines[:5]:  # cap at 5
                    print(f"  │     + \"{ex['line'][:50]}\"")
                if len(extra_lines) > 5:
                    print(f"  │     ... and {len(extra_lines) - 5} more")

            print(f"  └{'─' * 50}")

    print()


# ──────────────────── Main ────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=f'OCR Benchmark v{VERSION} — Multi-model comparison',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all models on two images with ground truth scoring
  python3 run_benchmark.py --images img1.jpg img2.jpg --ground-truth gt.json

  # Run only specific models
  python3 run_benchmark.py --images img1.jpg --models opus sonnet

  # Skip models whose env vars are missing (silent)
  python3 run_benchmark.py --images img1.jpg --auto-skip

  # Re-score without re-running OCR
  python3 run_benchmark.py --score-only --output-dir ./results --ground-truth gt.json
"""
    )
    parser.add_argument('--images', nargs='+', help='Image file paths to benchmark')
    parser.add_argument(
        '--models', nargs='+', default=DEFAULT_MODELS,
        choices=list(MODELS.keys()),
        help='Models to benchmark (default: all)'
    )
    parser.add_argument('--output-dir', default='./ocr-results', help='Output directory for JSON results')
    parser.add_argument('--ground-truth', help='Path to ground truth JSON for scoring')
    parser.add_argument('--score-only', action='store_true', help='Only score existing results, skip OCR')
    parser.add_argument(
        '--auto-skip', action='store_true',
        help='Silently skip models when required env vars are missing'
    )
    parser.add_argument('--version', action='version', version=f'OCR Benchmark {VERSION}')
    args = parser.parse_args()

    if not args.score_only and not args.images:
        parser.error('--images is required unless --score-only is set')

    os.makedirs(args.output_dir, exist_ok=True)

    # ── Score-only mode ──
    if args.score_only:
        if not args.ground_truth:
            parser.error('--ground-truth is required for --score-only')
        scores = score_results(args.output_dir, args.ground_truth, verbose=True)
        print_terminal_report(scores)
        return

    # ── Validate image paths ──
    for img_path in args.images:
        if not os.path.exists(img_path):
            print(f"ERROR: {img_path} not found", file=sys.stderr)
            sys.exit(1)

    # ── Resolve which models to run ──
    models_to_run = []
    skipped = []
    for mk in args.models:
        ok, missing = check_model_env(mk)
        if ok:
            models_to_run.append(mk)
        else:
            if args.auto_skip:
                skipped.append((mk, missing))
            else:
                # Non-fatal warning; skip and continue
                label = MODELS[mk]['label']
                print(f"⚠️  Skipping {label}: missing {', '.join(missing)}", file=sys.stderr)
                skipped.append((mk, missing))

    if skipped:
        print(f"\n⚠️  Skipped {len(skipped)} model(s) due to missing dependencies/env vars:")
        for mk, missing in skipped:
            print(f"   • {MODELS[mk]['label']}: {', '.join(missing)}")
        print()

    if not models_to_run:
        print("ERROR: No runnable models. Set required environment variables.", file=sys.stderr)
        sys.exit(1)

    total = len(args.images) * len(models_to_run)
    done = 0

    for img_path in args.images:
        img_name = os.path.splitext(os.path.basename(img_path))[0]
        for model_key in models_to_run:
            done += 1
            cfg = MODELS[model_key]
            print(f"[{done}/{total}] {img_name} × {cfg['label']}...", end=' ', flush=True)
            try:
                result = run_ocr(img_path, model_key)
                out_file = os.path.join(args.output_dir, f"{img_name}.{model_key}.json")
                with open(out_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                cost_in = result['input_tokens'] / 1_000_000 * cfg['input_price']
                cost_out = result['output_tokens'] / 1_000_000 * cfg['output_price']
                cost = cost_in + cost_out
                print(f"✅  {result['latency_seconds']}s  ${cost:.4f}  ({result['input_tokens']}→{result['output_tokens']} tok)")
            except Exception as e:
                print(f"❌  {e}")

    # ── Scoring ──
    if args.ground_truth:
        print("\n📊 Scoring against ground truth...")
        scores = score_results(args.output_dir, args.ground_truth, verbose=True)
        print_terminal_report(scores)
    else:
        print("\nℹ️  No --ground-truth provided. Run with --ground-truth gt.json to score results.")


if __name__ == '__main__':
    main()
