# Uploading Assets

Upload video, audio, or image files to use as inputs in agent runs.

## Procedure

1. **Get upload URL:** `POST /uploads/{type}/get_upload_url` (type: `video`, `audio`, `image`)
2. **Upload file:** PUT the file to the returned signed URL.
3. **Finalize:** `POST /uploads/{type}/finalize_upload` with the upload ID.
4. **Use in runs:** Pass the resulting asset UUID as `video_ids` in your run payload.

## Get a view URL

To get a temporary signed URL for an existing asset:

```
POST /uploads/get_view_url
```

## Docs

- [Upload flow overview](https://docs.mosaic.so/api/asset-management/upload-flow)
- [Video upload URL](https://docs.mosaic.so/api/asset-management/post-uploads-video-get-upload-url)
- [Finalize video](https://docs.mosaic.so/api/asset-management/post-uploads-video-finalize-upload)
- [Audio upload URL](https://docs.mosaic.so/api/asset-management/post-uploads-audio-get-upload-url)
- [Finalize audio](https://docs.mosaic.so/api/asset-management/post-uploads-audio-finalize-upload)
- [Image upload URL](https://docs.mosaic.so/api/asset-management/post-uploads-image-get-upload-url)
- [Finalize image](https://docs.mosaic.so/api/asset-management/post-uploads-image-finalize-upload)
- [Get view URL](https://docs.mosaic.so/api/asset-management/post-uploads-get-view-url)
