# Article presentation

Use the generic `document.article` presentation so compatible hosts can render the result without Skill-specific client code.

```json
{
  "type": "document.article",
  "version": 1,
  "data": {
    "platform": "wechat",
    "projectId": "content_xxx",
    "revision": 4,
    "status": "rendered",
    "title": "Article title",
    "author": "",
    "digest": "Article digest",
    "contentMarkdown": "# Article",
    "contentHtml": "<section>Formatted article</section>",
    "coverUrl": "https://assets.example/cover.jpg",
    "theme": "pixmind-clean",
    "imageCount": 3,
    "sources": [],
    "outline": {},
    "review": {}
  },
  "actions": [
    {
      "type": "command",
      "action": "copy.rich-text",
      "label": "复制到公众号编辑器"
    }
  ]
}
```

`copy.rich-text` is a local host action. Copy sanitized `contentHtml` as `text/html` and the visible article text as `text/plain`, then let the user paste into the WeChat Official Account editor. It must not call a remote publication API.

`contentHtml` must contain portable inline styles because the WeChat editor does not load Builder CSS. `coverUrl` may be empty for a text-only article; this must not prevent rendering or the copy action.

If the host does not support this presentation, show the title, digest, Markdown body, image briefs, sources, review issues, project ID, and revision as normal conversation content, and expose the rendered HTML as a copyable artifact.
