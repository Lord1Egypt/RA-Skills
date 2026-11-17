"""Paged-report generator package."""

__all__ = ["ReportValidationError", "render_report"]


def __getattr__(name):
    if name in __all__:
        from .paged_report import ReportValidationError, render_report

        return {"ReportValidationError": ReportValidationError, "render_report": render_report}[name]
    raise AttributeError(name)
