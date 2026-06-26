"""LinkedIn post submission."""

from __future__ import annotations

import logging

from .bridge import BridgePage
from .errors import PublishError
from .human import sleep_random
from .selectors import IMAGE_ATTACH, POST_EDITOR, POST_SUBMIT, SHARE_BOX_TRIGGER
from .types import SubmitPostContent
from .urls import HOME_URL

logger = logging.getLogger(__name__)


def submit_text_post(page: BridgePage, content: SubmitPostContent) -> None:
    """Submit a text post to the LinkedIn feed."""
    _open_share_box(page)
    _fill_post_editor(page, content.text)
    _click_post_button(page)
    logger.info("Text post submitted to LinkedIn feed")


def submit_image_post(page: BridgePage, content: SubmitPostContent) -> None:
    """Submit an image post to the LinkedIn feed."""
    if not content.images:
        raise PublishError("No images provided for image post")

    _open_share_box(page)
    _attach_images(page, content.images)

    if content.text:
        _fill_post_editor(page, content.text)

    _click_post_button(page)
    logger.info("Image post submitted to LinkedIn feed")


def _open_share_box(page: BridgePage) -> None:
    """Navigate to feed and open the share creation dialog."""
    page.navigate(HOME_URL)
    page.wait_for_load()
    page.wait_dom_stable()
    sleep_random(500, 1000)

    page.wait_for_element(SHARE_BOX_TRIGGER, timeout=15.0)
    page.click_element(SHARE_BOX_TRIGGER)
    sleep_random(800, 1500)

    # Wait for the post editor to appear inside the modal
    page.wait_for_element(POST_EDITOR, timeout=15.0)
    sleep_random(300, 600)


def _fill_post_editor(page: BridgePage, text: str) -> None:
    """Fill the post editor with text content."""
    page.click_element(POST_EDITOR)
    sleep_random(200, 400)
    page.input_content_editable(POST_EDITOR, text)
    sleep_random(300, 600)


def _attach_images(page: BridgePage, image_paths: list[str]) -> None:
    """Attach one or more images to the post via the toolbar."""
    try:
        page.wait_for_element(IMAGE_ATTACH, timeout=10.0)
        page.click_element(IMAGE_ATTACH)
        sleep_random(600, 1000)

        # LinkedIn uses a hidden file input for image upload
        page.set_file_input('input[type="file"]', image_paths)
        sleep_random(2000, 3500)  # Wait for upload preview to render
    except Exception as e:
        raise PublishError(f"Failed to attach images: {e}") from e


def _click_post_button(page: BridgePage) -> None:
    """Click the Post button and confirm the editor closed."""
    page.evaluate("window.onbeforeunload = null;")

    page.wait_for_element(POST_SUBMIT, timeout=10.0)

    for attempt in range(3):
        try:
            page.click_element(POST_SUBMIT)
            sleep_random(1500, 2500)

            if not page.has_element(POST_EDITOR):
                logger.info("Post submitted — editor closed")
                return

            sleep_random(500, 1000)
        except Exception as e:
            if attempt == 2:
                raise PublishError(f"Failed to click post button: {e}") from e
            sleep_random(500, 1000)

    raise PublishError("Post button clicked but editor remained open")
