"""LinkedIn automation exception hierarchy."""


class LinkedInError(Exception):
    """Base exception for LinkedIn automation."""


class BridgeError(LinkedInError):
    """Bridge communication error."""


class NoPostsError(LinkedInError):
    """No posts captured."""

    def __init__(self) -> None:
        super().__init__("No posts captured from page")


class NoPostDetailError(LinkedInError):
    """No post detail captured."""

    def __init__(self) -> None:
        super().__init__("No post detail captured")


class NotLoggedInError(LinkedInError):
    """Not logged in."""

    def __init__(self) -> None:
        super().__init__(
            "Not logged in. Please log in to LinkedIn in your browser first."
        )


class PublishError(LinkedInError):
    """Publish failed."""


class InteractionError(LinkedInError):
    """Interaction (like, comment, connect, message) failed."""


class ElementNotFoundError(LinkedInError):
    """Element not found on page."""

    def __init__(self, selector: str) -> None:
        self.selector = selector
        super().__init__(f"Element not found: {selector}")
