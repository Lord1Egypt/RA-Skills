"""LinkedIn social interactions: like, comment, connect, message."""

from __future__ import annotations

import logging

from .bridge import BridgePage
from .human import sleep_random
from .selectors import (
    COMMENT_BTN,
    COMMENT_EDITOR,
    COMMENT_SUBMIT,
    LIKE_BUTTON,
    MSG_COMPOSE_EDITOR,
    MSG_SEND_BTN,
    PROFILE_CONNECT_BTN,
    PROFILE_MESSAGE_BTN,
)
from .types import ActionResult
from .urls import make_post_url, make_profile_url

logger = logging.getLogger(__name__)


def like_post(page: BridgePage, post_url: str) -> ActionResult:
    """Like a LinkedIn post.

    Args:
        page: BridgePage instance.
        post_url: Full post URL or URN.

    Returns:
        ActionResult indicating success or failure.
    """
    url = make_post_url(post_url)
    page.navigate(url)
    page.wait_for_load()
    page.wait_dom_stable()
    sleep_random(500, 1000)

    try:
        page.wait_for_element(LIKE_BUTTON, timeout=15.0)
        page.click_element(LIKE_BUTTON)
        sleep_random(300, 600)
        logger.info("Post liked: %s", url)
        return ActionResult(success=True, message="Post liked", url=url)
    except Exception as e:
        logger.error("Like failed: %s", e)
        return ActionResult(success=False, message=str(e), url=url)


def comment_post(page: BridgePage, post_url: str, content: str) -> None:
    """Post a comment on a LinkedIn post.

    Args:
        page: BridgePage instance.
        post_url: Full post URL or URN.
        content: Comment text.
    """
    url = make_post_url(post_url)
    page.navigate(url)
    page.wait_for_load()
    page.wait_dom_stable()
    sleep_random(500, 1000)

    # Click the "Comment" button to reveal the comment box
    try:
        page.wait_for_element(COMMENT_BTN, timeout=15.0)
        page.click_element(COMMENT_BTN)
        sleep_random(600, 1000)
    except Exception:
        logger.debug("No comment trigger button — trying direct editor access")

    # Fill in the comment
    page.wait_for_element(COMMENT_EDITOR, timeout=15.0)
    page.click_element(COMMENT_EDITOR)
    sleep_random(200, 400)
    page.input_content_editable(COMMENT_EDITOR, content)
    sleep_random(300, 600)

    # Submit
    page.wait_for_element(COMMENT_SUBMIT, timeout=10.0)
    page.click_element(COMMENT_SUBMIT)
    sleep_random(1000, 1500)

    logger.info("Comment posted on: %s", url)


def send_connection_request(
    page: BridgePage,
    profile_url: str,
    note: str = "",
) -> ActionResult:
    """Send a connection request to a LinkedIn profile.

    Args:
        page: BridgePage instance.
        profile_url: Profile URL or slug.
        note: Optional personalised connection note (max 300 chars).

    Returns:
        ActionResult indicating success or failure.
    """
    url = make_profile_url(profile_url)
    page.navigate(url)
    page.wait_for_load()
    page.wait_dom_stable()
    sleep_random(800, 1500)

    try:
        page.wait_for_element(PROFILE_CONNECT_BTN, timeout=15.0)
        page.click_element(PROFILE_CONNECT_BTN)
        sleep_random(600, 1000)

        # The "Add a note" dialog may appear
        add_note_btn = 'button[aria-label*="Add a note"]'
        send_without_note_btn = (
            'button[aria-label*="Send without a note"], '
            'button[aria-label="Send now"]'
        )
        send_with_note_btn = (
            'button[aria-label="Send invitation"], '
            'button[aria-label="Send"]'
        )

        if note and page.has_element(add_note_btn):
            page.click_element(add_note_btn)
            sleep_random(400, 700)
            note_field = 'textarea#custom-message, textarea[name="message"]'
            page.input_text(note_field, note[:300])  # LinkedIn cap: 300 chars
            sleep_random(300, 600)
            page.click_element(send_with_note_btn)
        elif page.has_element(send_without_note_btn):
            page.click_element(send_without_note_btn)
        elif page.has_element(send_with_note_btn):
            page.click_element(send_with_note_btn)

        sleep_random(800, 1200)
        logger.info("Connection request sent to %s", url)
        return ActionResult(success=True, message="Connection request sent", url=url)

    except Exception as e:
        logger.error("Connection request failed: %s", e)
        return ActionResult(success=False, message=str(e), url=url)


def send_message(
    page: BridgePage,
    profile_url: str,
    message_text: str,
) -> ActionResult:
    """Send a direct message to a LinkedIn connection.

    Args:
        page: BridgePage instance.
        profile_url: Profile URL or slug of the recipient.
        message_text: Message body.

    Returns:
        ActionResult indicating success or failure.
    """
    url = make_profile_url(profile_url)
    page.navigate(url)
    page.wait_for_load()
    page.wait_dom_stable()
    sleep_random(800, 1500)

    try:
        page.wait_for_element(PROFILE_MESSAGE_BTN, timeout=15.0)
        page.click_element(PROFILE_MESSAGE_BTN)
        sleep_random(1000, 1500)

        # Wait for the messaging overlay to open
        page.wait_for_element(MSG_COMPOSE_EDITOR, timeout=15.0)
        page.click_element(MSG_COMPOSE_EDITOR)
        sleep_random(300, 600)
        page.input_content_editable(MSG_COMPOSE_EDITOR, message_text)
        sleep_random(400, 700)

        page.wait_for_element(MSG_SEND_BTN, timeout=10.0)
        page.click_element(MSG_SEND_BTN)
        sleep_random(800, 1200)

        logger.info("Message sent to %s", url)
        return ActionResult(success=True, message="Message sent", url=url)

    except Exception as e:
        logger.error("Message failed: %s", e)
        return ActionResult(success=False, message=str(e), url=url)
