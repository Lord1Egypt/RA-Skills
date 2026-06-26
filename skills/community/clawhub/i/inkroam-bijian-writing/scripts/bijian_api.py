#!/usr/bin/env python3
import argparse
import json
import os
import sys
from urllib.parse import urlencode
import urllib.request
import urllib.error


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def bool_str(v: str) -> bool:
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    if s in {"1", "true", "yes", "y", "on"}:
        return True
    if s in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError(f"invalid bool: {v}")


class BijianClient:
    def __init__(self):
        self.base_url = env("BIJIAN_BASE_URL", "https://bj.aizmjx.com/api").rstrip("/")
        self.token = env("BIJIAN_API_TOKEN")
        self.token_header = env("BIJIAN_TOKEN_HEADER", "Authorization")
        self.token_prefix = env("BIJIAN_TOKEN_PREFIX", "Bearer")
        self.user_id = env("BIJIAN_USER_ID")

    def _headers(self):
        h = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.token:
            if self.token_prefix:
                h[self.token_header] = f"{self.token_prefix} {self.token}".strip()
            else:
                h[self.token_header] = self.token
        return h

    def _request(self, method: str, path: str, query=None, body=None):
        query = dict(query or {})
        # fallback user context (for endpoints expecting injected userId)
        if self.user_id and "userId" not in query:
            query["userId"] = self.user_id

        url = f"{self.base_url}{path}"
        if query:
            url = f"{url}?{urlencode(query)}"

        data = None
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")

        req = urllib.request.Request(url=url, data=data, headers=self._headers(), method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")
                return resp.getcode(), self._maybe_json(raw)
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="ignore") if e.fp else str(e)
            return e.code, self._maybe_json(raw)
        except Exception as e:
            return 0, {"error": str(e)}

    @staticmethod
    def _maybe_json(raw: str):
        try:
            return json.loads(raw)
        except Exception:
            return {"raw": raw}

    def get_spaces(self):
        return self._request("GET", "/bj/v1/spaces")

    def get_styles(self, platform_code: str):
        return self._request("GET", f"/bj/v1/style-groups/user/{platform_code}")

    def generate(self, payload: dict):
        return self._request("POST", "/bj/v1/article/generateContent", body=payload)

    def task_status(self, article_id: int):
        return self._request("GET", "/bj/v1/article/pollTaskStatus", query={"articleId": article_id})

    def get_article(self, article_id: int):
        return self._request("GET", "/bj/v1/article/getArticleById", query={"articleId": article_id})

    def get_articles_by_space(self, space_id: int, current: int, size: int, keyword: str = ""):
        query = {"spaceId": space_id, "current": current, "size": size}
        if keyword:
            query["keyword"] = keyword
        return self._request("GET", "/bj/v1/article/getArticleListBySpaceId", query=query)


def print_json(code, payload):
    out = {"http": code, "result": payload}
    print(json.dumps(out, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description="Bijian Content API CLI")
    sp = p.add_subparsers(dest="cmd", required=True)

    sp.add_parser("spaces", help="List spaces")

    s_styles = sp.add_parser("styles", help="List styles by platform")
    s_styles.add_argument("--platform-code", required=True, help="e.g. wxgzh")

    s_gen = sp.add_parser("generate", help="Generate article by space requirements")
    s_gen.add_argument("--space-id", type=int, required=True)
    s_gen.add_argument("--style-group-id", type=int, default=None)
    s_gen.add_argument("--model-id", type=int, default=None)
    s_gen.add_argument("--platform-code", default="wxgzh")
    s_gen.add_argument("--topic-theme", required=True)
    s_gen.add_argument("--viewpoints", default="", help="观点要点，建议3-5条")
    s_gen.add_argument("--reference-content", default="")
    s_gen.add_argument("--user-require", default="")
    s_gen.add_argument("--is-regenerate", default="true")
    s_gen.add_argument("--is-need-picture", default="false")

    s_task = sp.add_parser("task", help="Poll task status")
    s_task.add_argument("--article-id", type=int, required=True)

    s_article = sp.add_parser("article", help="Get article detail")
    s_article.add_argument("--article-id", type=int, required=True)

    s_articles = sp.add_parser("articles", help="List articles by space")
    s_articles.add_argument("--space-id", type=int, required=True)
    s_articles.add_argument("--current", type=int, default=1)
    s_articles.add_argument("--size", type=int, default=10)
    s_articles.add_argument("--keyword", default="")

    args = p.parse_args()
    c = BijianClient()

    if args.cmd == "spaces":
        code, payload = c.get_spaces()
        print_json(code, payload)
        return

    if args.cmd == "styles":
        code, payload = c.get_styles(args.platform_code)
        print_json(code, payload)
        return

    if args.cmd == "generate":
        # three-input guard: topic required; viewpoints/reference recommended
        if not str(args.topic_theme).strip():
            print_json(400, {"error": "topicTheme(主题)必填"})
            return

        user_require = (args.user_require or "").strip()
        viewpoints = (args.viewpoints or "").strip()
        if viewpoints:
            if user_require:
                user_require = f"观点要点：{viewpoints}\n\n{user_require}"
            else:
                user_require = f"观点要点：{viewpoints}"

        if not viewpoints and not (args.reference_content or "").strip() and not user_require:
            print_json(422, {
                "error": "请先补齐三要素：主题(必填)、观点要点、参考素材。当前缺少观点要点/参考素材。"
            })
            return

        payload = {
            "spaceId": args.space_id,
            "styleGroupId": args.style_group_id,
            "modelId": args.model_id,
            "platformCode": args.platform_code,
            "topicTheme": args.topic_theme,
            "referenceContent": args.reference_content,
            "userRequire": user_require,
            "isRegenerate": bool_str(args.is_regenerate),
            "isNeedPicture": bool_str(args.is_need_picture),
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        code, res = c.generate(payload)
        print_json(code, res)
        return

    if args.cmd == "task":
        code, payload = c.task_status(args.article_id)
        print_json(code, payload)
        return

    if args.cmd == "article":
        code, payload = c.get_article(args.article_id)
        print_json(code, payload)
        return

    if args.cmd == "articles":
        code, payload = c.get_articles_by_space(args.space_id, args.current, args.size, args.keyword)
        print_json(code, payload)
        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
