BASE_URL = "https://learn.hoseo.ac.kr"
USER_AGENT = "Mozilla/5.0"

CREDENTIALS_PATH = "~/.config/hoseo_lms/credentials.json"
DATA_PATH = "~/.config/hoseo_lms/data.json"

LMS_PATHS = {
    "login": "/login/index.php",
    "course_list": "/local/ubion/user/index.php",
    "attendance": "/local/ubonattend/my_status.php",
    "assignments": "/mod/assign/index.php",
    "quizzes": "/mod/quiz/index.php",
}

SUBMISSION_KEYWORDS = ("submitted", "\uc81c\ucd9c")  # LMS locale-dependent

UNAVAILABLE_DIALOG_KEYWORD = "\uc5f4\ub78c\uc774 \ubd88\uac00\ub2a5\ud569\ub2c8\ub2e4"  # LMS dialog text

