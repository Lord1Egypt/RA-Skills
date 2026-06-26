from atproto import Client, client_utils, models

class BlueskyAgent:
    def __init__(self, pds_url="https://bsky.social"):
        self.client = Client(base_url=pds_url)

    def login(self, identifier, app_password):
        """Authenticates using an App Password."""
        self.client.login(identifier, app_password)
        return self.client.get_profile(actor=identifier)

    def post(self, text, reply_to=None, embed=None):
        """
        Creates a post. 
        reply_to expects a dict with 'root' (uri/cid) and 'parent' (uri/cid) strong refs.
        """
        if reply_to:
            root_ref = models.create_strong_ref(reply_to['root'])
            parent_ref = models.create_strong_ref(reply_to['parent'])
            return self.client.send_post(
                text=text,
                reply_to=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref)
            )
        return self.client.send_post(text=text)

    def upload_image(self, image_bytes, alt_text, mimetype="image/jpeg"):
        """Uploads an image blob and returns the reference."""
        return self.client.upload_blob(image_bytes, encoding=mimetype)

    def bookmark(self, uri, cid):
        """Private bookmarking."""
        return self.client.app.bsky.bookmark.create_bookmark(
            data={"subject": {"uri": uri, "cid": cid}}
        )

    def resolve_handle(self, handle):
        """Resolves a handle to a DID."""
        return self.client.resolve_handle(handle)
