# Social Publishing

Connect social accounts and publish edited videos directly from the API.

## Procedure

1. **Connect account:** `POST /social/{platform}/connect`
2. **Run agent** and wait for `outputs[].video_url` in the completed run.
3. **Publish:** `POST /social/post` with `media_urls` pointing to the output.
4. **Track:** Poll `GET /social/post/{post_id}` or `GET /social/post/track/{tracking_id}`.

## Supported platforms

`youtube`, `tiktok`, `instagram`, `facebook`, `linkedin`, `x`

## Connect a platform

```
POST /social/{platform}/connect
```

[Docs](https://docs.mosaic.so/api/social/post-social-platform-connect)

## Check connection status

```
GET /social/{platform}/status
```

[Docs](https://docs.mosaic.so/api/social/get-social-platform-status)

## Disconnect a platform

```
DELETE /social/{platform}/remove
```

[Docs](https://docs.mosaic.so/api/social/delete-social-platform-remove)

## Create a post

```json
POST /social/post
{
  "platform": "youtube",
  "media_urls": ["https://...output_video_url..."],
  "title": "My Edited Video",
  "description": "Published via Mosaic API"
}
```

[Docs](https://docs.mosaic.so/api/social/post-social-post)

## Track post status

- `GET /social/post/{post_id}` — [Docs](https://docs.mosaic.so/api/social/get-social-post)
- `GET /social/post/track/{tracking_id}` — [Docs](https://docs.mosaic.so/api/social/get-social-post-track)

## Update / delete a post

- `PATCH /social/post/{post_id}` — [Docs](https://docs.mosaic.so/api/social/patch-social-post)
- `DELETE /social/post/{post_id}` — [Docs](https://docs.mosaic.so/api/social/delete-social-post)
