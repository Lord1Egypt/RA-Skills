---
name: manage-media-library
description: Upload images and videos to the Auto Poster AI media library and browse what is already there. Use when the user wants to add a photo or video, attach media to a post, reuse a past image, or upload a large video file.
---

# Manage the media library

Uses `autoposter_upload_media`, `autoposter_create_upload_link`, `autoposter_get_media_upload_url` and `autoposter_list_media`.

## Pick the upload path

1. **Public image or video URL, or a data URI:** `autoposter_upload_media` with `url`. Returns the library item and a public CDN URL.
2. **File object from the client:** `autoposter_upload_media` with `file`. Limit is 100 MB.
3. **Image exists only on the user's device or in chat, and you cannot send its bytes:** `autoposter_create_upload_link`. Give the user the link, wait until they say the upload is done, then call `autoposter_list_media` (newest first) and take the new item's ID.
4. **Video over 100 MB:** if you can make an HTTP PUT or multipart POST, call `autoposter_get_media_upload_url` with `fileName` and `contentType` (for example `video/mp4`), upload to the returned URL, and use the returned CDN URL. Chat-only clients cannot do this: ask the user for a direct public file URL instead. Upload limit is 5 GB.

## Browse and reuse

- `autoposter_list_media` with `type` (`image` or `video`) and `limit` (max 50). Show name, type and URL.
- Attach library items to a post with `mediaIds`, or public URLs with `mediaUrls`, through `schedule-social-posts`.

## Rules

- Check `autoposter_get_rules` for the target platform's media format and size limits before uploading. Reels and Shorts need video; Stories need image or video.
- After an upload, confirm the item shows up in `autoposter_list_media` before attaching it.
- You cannot delete media: there is no tool for it. If the user asks, tell them to remove it in Auto Poster AI.
