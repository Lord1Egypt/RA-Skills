class HRSkillError(Exception):
    """An expected, user-facing skill error."""

    def __init__(self, code: str, message: str, details: object | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details
