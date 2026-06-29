#!/usr/bin/env python3

"""

Theme clustering for ranked papers.

Groups top-N papers into 3-5 thematic sub-categories based on titles + AI rerank reasons.

Outputs themed JSON with _theme field + thematically grouped Markdown.

"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json, os, sys, argparse, urllib.request, urllib.error

from pathlib import Path



from utils.pipeline_schema import validate, report, stamp, check_version, PIPELINE_VERSION



import sys, os




DEFAULT_MODEL = "deepseek-v4-pro"

DEFAULT_BASE_URL = "https://api.deepseek.com"



def load_api_config():

    """从 OpenClaw 配置文件或环境变量加载 API 凭证。优先级：环境变量 > openclaw.json > 默认值"""

    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")

    base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("DEEPSEEK_BASE_URL")

    if api_key and base_url:

        return api_key, base_url



    config_paths = [Path.home() / ".openclaw" / "openclaw.json"]

    for cf in config_paths:

        if cf.exists():

            try:

                config = json.load(open(cf, encoding="utf-8"))

                providers = config.get("models", {}).get("providers", {})

                for name in ["custom-api-deepseek-com", "moonshot"]:

                    p = providers.get(name, {})

                    if p.get("apiKey") and p.get("baseUrl"):

                        return p["apiKey"], p["baseUrl"]

                for p in providers.values():

                    if p.get("apiKey") and p.get("baseUrl"):

                        return p["apiKey"], p["baseUrl"]

            except Exception:

                pass

    return None, None



def cluster_papers(papers, topic, api_key=None, base_url=None, model=None):

    """Use AI to cluster papers into thematic groups."""



    # Resolve API config

    if not api_key or not base_url:

        key, url = load_api_config()

        api_key = api_key or key

        base_url = base_url or url



    if not api_key or not base_url:

        print("[ThemeCluster] No API config found - fallback to single theme", file=sys.stderr)

        return {"themes": [{"name": topic, "papers": list(range(1, len(papers)+1)), "description": ""}]}



    model = model or DEFAULT_MODEL



    # Build prompt with paper titles and reasons

    paper_desc = []

    for i, p in enumerate(papers):

        title = p.get('title', '?')

        ai = p.get('_ai_scores', {})

        reason = ai.get('reason', '')

        paper_desc.append(f"{i+1}. {title}\n   {reason}")



    prompt = f"""Group the following {len(papers)} papers about "{topic}" into 3-5 thematic sub-categories.



For each paper, assign exactly one theme. Theme names MUST be in Chinese (6-12 characters each), describing the core research direction.



Papers:

{chr(10).join(paper_desc)}



Return JSON only, no explanation:

{{"themes": [

  {{"name": "Theme name (Chinese, 6-12 chars)", "papers": [1, 3, 7], "description": "one sentence about this theme"}}

]}}



Rules:

- Every paper number must appear exactly once

- 3-5 themes total

- Group by actual research focus, not by database or venue

- Theme names MUST be in Chinese

- If a paper doesn't clearly fit any theme, put it in "交叉与其它"""



    api_url = base_url.rstrip('/') + '/chat/completions'



    payload = json.dumps({

        "model": model,

        "messages": [{"role": "user", "content": prompt}],

        "temperature": 0.3,

        "max_tokens": 2000,

        "thinking": {"type": "disabled"}

    }).encode('utf-8')



    req = urllib.request.Request(

        api_url,

        data=payload,

        headers={

            "Content-Type": "application/json",

            "Authorization": f"Bearer {api_key}"

        },

        method="POST"

    )



    try:

        with urllib.request.urlopen(req, timeout=30) as resp:

            raw = resp.read().decode('utf-8')

            result = json.loads(raw)

            content = result['choices'][0]['message']['content']

            # Strip markdown code fences if present

            if content.startswith('```'):

                content = content.split('\n', 1)[1]

                if content.endswith('```'):

                    content = content[:-3]

            return json.loads(content)

    except urllib.error.HTTPError as e:

        body = e.read().decode('utf-8', errors='replace')

        print(f"[ThemeCluster] HTTP {e.code}: {body[:300]}", file=sys.stderr)

    except Exception as e:

        print(f"[ThemeCluster] Error: {e}", file=sys.stderr)

    return {"themes": [{"name": topic, "papers": list(range(1, len(papers)+1)), "description": ""}]}



def main():

    parser = argparse.ArgumentParser(description="Cluster papers into thematic groups")

    parser.add_argument('-i', '--input', required=True, help='Input JSON (summarized.json or ai_ranked.json)')

    parser.add_argument('-o', '--output', help='Output JSON file')

    parser.add_argument('--top', type=int, default=15, help='Top N papers')

    parser.add_argument('-t', '--topic', required=True, help='Research topic')

    parser.add_argument('--api-key', help='API key')

    parser.add_argument('--base-url', help='API base URL')

    parser.add_argument('--model', help='Model name')

    args = parser.parse_args()



    d = json.load(open(args.input, encoding='utf-8'))

    papers = d.get('papers', d if isinstance(d, list) else [])[:args.top]



    print(f"[ThemeCluster] Clustering {len(papers)} papers on: {args.topic}")

    result = cluster_papers(papers, args.topic, args.api_key, args.base_url, args.model)



    themes = result.get('themes', [])



    # Assign _theme to each paper

    paper_index = {i+1: p for i, p in enumerate(papers)}

    for theme in themes:

        for paper_num in theme.get('papers', []):

            if paper_num in paper_index:

                paper_index[paper_num]['_theme'] = theme['name']



    # Build themed output

    output = {

        'total': len(papers),

        'themes': themes,

        'papers': papers

    }



    # --- 校验 + 报告 ---

    ok, issues = validate(papers, stage="themed")

    if issues:

        report(issues, stage="themed")



    if args.output:

        os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)

        stamp(output, stage="themed")

        with open(args.output, 'w', encoding='utf-8') as f:

            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"[ThemeCluster] {len(themes)} themes → {args.output}")



    # Print theme summary

    for theme in themes:

        papers_in_theme = [i for i in theme['papers'] if i in paper_index]

        print(f"  {theme['name']}: {len(papers_in_theme)} papers")



    return output



if __name__ == '__main__':

    main()

