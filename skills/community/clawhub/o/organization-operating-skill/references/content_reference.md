# Content Reference

## When to Read

- When publishing a post inside an organization
- When confirming the post share-link pattern
- When investigating why post read endpoints behave differently from post write endpoints

## Related Capabilities

| Capability ID | API | Method |
| --- | --- | --- |
| `content.post.create` | `/outer/api/proxy/meta/api/v1/content/article/create` | `POST` |

## `content.post.create`

- Endpoint: `POST /outer/api/proxy/meta/api/v1/content/article/create`
- Authentication: yes
- Recommended headers:
  - `Authorization`
  - `x-platform=3`
  - `x-device-id`
  - `x-device_id`
  - `x-timezone`
  - `x-version`
  - `x-buildnumber`
  - `x-brand`
  - `x-model`
  - `x-system-version`
  - `x-system_version`
- Minimum request body:
  - `orgId`
  - `article.richText`
  - `article.visibled`
  - `article.vcmUids`
  - `saasList`

Minimum example:

```json
{
  "orgId": 1141,
  "article": {
    "richText": [
      { "insert": "Agent post for post-publishing verification.\n" }
    ],
    "visibled": 0,
    "vcmUids": []
  },
  "saasList": []
}
```

## Confirmed Behavior

- The proxy layer performs camelCase and snake_case conversion.
- The `post-create` command already includes the required extra web headers.
- The current write endpoint is more stable than the read endpoints.
- What the product currently calls a "help post" is still just a normal post; there is no separate API for it.
- In the test environment, prefer returning a `sharePost` page link for manual verification.

## Read Limitations

- The backend does have `ContentArticleOuterControllerV1`.
- In the test environment, direct calls to post detail or list endpoints through generic requests may still return:
  - `code=1144`
  - `msg=System error.`
- That means the current first-phase skill should treat post support as a write-first workflow.

## Share Links

Server share-base configuration:

- Production: `https://share.zingup.club/`
- Test and local: `https://test-share.groupoo.net/`

Recommended SSR rule for post share links:

```text
{shareBase}ssr/sharePost/{articleId}?id={articleId}&t2=1&t8=ch
```

Additional validation notes:

- A historically verified test-environment link, `https://test-web.groupoo.net/ssr/sharePost/{articleId}?id={articleId}&t2=1&t8=ch`, can also open the share page.
- The `sharePost` page title directly shows a summary of the post body.
- `shareArticle` and `shareDynamic` can open pages in the current test environment, but their content hit rate is weaker than `sharePost`.

Configuration source:

- `application-prod.yml`: `biz-config.share.url=https://share.zingup.club/`
- `application-test.yml` and `application-local.yml`: `biz-config.share.url=https://test-share.groupoo.net/`

## Common CLI Commands

```bash
python scripts/org_skill_cli.py --env test post-create --org-id 1141 --text "Looking for one volunteer photographer for the event."
```

## Code Locations

- Proxy controller: `biz-service/.../ProxyController.java`
- Post outer controller: `biz-service/.../ContentArticleOuterControllerV1.java`
