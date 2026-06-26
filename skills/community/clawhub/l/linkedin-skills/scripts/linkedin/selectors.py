"""LinkedIn page CSS selectors.

These target LinkedIn (www.linkedin.com) as of 2025-2026.
LinkedIn uses a React SPA — selectors use data attributes and stable class names.
Selectors may need updating if LinkedIn redesigns its frontend.
"""

# ========== Auth ==========
LOGGED_IN_NAV = (
    "#global-nav .global-nav__me, "
    ".global-nav__nav .global-nav__me-photo"
)
NOT_LOGGED_IN = (
    ".authwall-join-form, "
    'a[href*="linkedin.com/login"], '
    ".join-now"
)

# ========== Feed ==========
# LinkedIn 2025+: uses hashed CSS classes; use stable aria-label anchor instead
FEED_POST = 'button[aria-label^="Open control menu for post by"]'

# ========== Search ==========
# LinkedIn 2025+: entity-result CSS gone; use stable href patterns
SEARCH_RESULT = 'a[href*="/in/"], a[href*="/company/"]'
SEARCH_RESULT_TITLE = 'span[aria-hidden="true"]'

# ========== Profile ==========
# LinkedIn 2025+: no h1 on profiles; name is in first section of main
PROFILE_NAME = "main section:first-of-type"
PROFILE_HEADLINE = "main section:first-of-type"
PROFILE_CONNECT_BTN = (
    'button[aria-label*="Connect with"], '
    'a[aria-label*="Invite"][aria-label*="to connect"], '
    'button[aria-label*="Connect"]'
)
PROFILE_MESSAGE_BTN = (
    'button[aria-label*="Message"], '
    'a[aria-label*="Message"]'
)

# ========== Company ==========
COMPANY_NAME = "main section:first-of-type h1"
COMPANY_TAGLINE = "main section:first-of-type"

# ========== Reactions ==========
LIKE_BUTTON = (
    "button.reactions-react-button, "
    'button[aria-label*="React Like"], '
    'button[aria-label="Like"]'
)

# ========== Comments ==========
COMMENT_BTN = (
    "button.comment-button, "
    'button[aria-label*="comment"], '
    'button[aria-label*="Comment"]'
)
COMMENT_EDITOR = (
    '.comments-comment-box .ql-editor[contenteditable="true"], '
    '.comments-comment-box--cr-redesign .ql-editor'
)
COMMENT_SUBMIT = "button.comments-comment-box__submit-button"

# ========== Share/Publish ==========
SHARE_BOX_TRIGGER = ".share-box-feed-entry__trigger"
POST_EDITOR = (
    '.share-creation-state .ql-editor[contenteditable="true"], '
    '.share-creation-state__editor .ql-editor'
)
POST_SUBMIT = "button.share-actions__primary-action"
IMAGE_ATTACH = (
    ".share-creation-state__toolbar button[aria-label*='photo'], "
    ".share-creation-state__toolbar button[aria-label*='Photo'], "
    ".share-creation-state__toolbar button[aria-label*='image']"
)

# ========== Messaging ==========
MSG_COMPOSE_EDITOR = (
    '.msg-form__contenteditable[contenteditable="true"], '
    '.msg-form__msg-content-container .ql-editor'
)
MSG_SEND_BTN = 'button.msg-form__send-button, button[aria-label="Send"]'
