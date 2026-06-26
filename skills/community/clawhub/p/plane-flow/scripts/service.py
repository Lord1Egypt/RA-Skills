from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

try:
    from .client import PlaneClient, PlaneAPIError
    from .config import Settings
except ImportError:
    from client import PlaneClient, PlaneAPIError
    from config import Settings


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

_MARKDOWN_RE = re.compile(
    r"(^"
    r"|\[.+?\]\(.+?\)"  # [text](url)
    r"|!\[.*?\]\(.*?\)"  # ![alt](url)
    r"|``"
    r"|`[^`\n]+`"
    r"|^#{1,6}\s"
    r"|^\s*[-*+]\s"
    r"|^\s*\d+\.\s"
    r"|\*\*[^*]+\*\*"
    r"|(?<!\*)\*[^*@]+\*(?!\*)"
    r")",
    re.MULTILINE | re.ASCII,
)


def _is_markdown(text: str) -> bool:
    return bool(_MARKDOWN_RE.search(text))


def render_markdown(text: str) -> str:
    """Convert markdown to HTML. Handles [image: path, align] directives before rendering.

    Directive syntax:
      [image: ./a.png]           – centred block
      [image: ./a.png, left]    – float left
      [image: ./a.png, right]   – float right
      [image: ./a.png, wrap]    – float left, text wraps right

    Note: inline directive processing requires project_id, issue_id and an upload
    function — use render_markdown_with_inline_images() directly when those are
    available.  This fallback renders directives as HTML placeholders.
    """
    if not text:
        return ""
    # Normalise literal \\n sequences to actual newlines before rendering
    text = text.replace(r"\n", "\n")

    # Replace directives with HTML img tags (fallback when upload info unavailable)
    def _replace_directive(match: re.Match) -> str:
        name = match.group(1).strip().rsplit("/", 1)[-1]
        align = (match.group(2) or "center").strip().lower()
        return _build_image_html("", align, name)

    text = _IMAGE_DIRECTIVE_RE.sub(_replace_directive, text)

    if not _is_markdown(text):
        return f"<p>{text}</p>"
    try:
        import markdown
        return markdown.markdown(
            text,
            extensions=["tables", "fenced_code", "nl2br"],
        )
    except Exception:
        return f"<p>{text}</p>"


# ---------------------------------------------------------------------------
# Inline image directive (rich positioning)
# ---------------------------------------------------------------------------

import re

_IMAGE_DIRECTIVE_RE = re.compile(
    r"\[image\s*:\s*([^\]]+?)\s*(?:,\s*(left|center|right|wrap))?\s*\]",
    re.IGNORECASE,
)


def _build_image_html(
    src: str,
    align: str,
    name: str,
) -> str:
    """Return a Plane-native image-component node for the Tiptap editor.

    Plane uses a custom <image-component> Tiptap node (atom block) that accepts
    an "alignment" attribute ("left" | "center" | "right").
    The src should be the full URL so the editor can reach it directly.
    A width hint is passed to give the editor a starting size.
    """
    align = (align or "center").lower()
    if align not in ("left", "center", "right"):
        align = "center"
    return (
        f'<image-component alignment="{align}" '
        f'src="{src}" '
        f'width="500" />'
    )



def render_markdown_with_inline_images(
    text: str,
    upload_func,
    project_id: str,
    issue_id: str,
    base_url: str,
) -> str:
    """Render markdown text, processing [image: path, align] directives.

    Supported directive forms:
      [image: ./a.png]             – center (default)
      [image: ./a.png, left]        – float left
      [image: ./a.png, right]       – float right
      [image: ./a.png, center]     – centered block
      [image: ./a.png, wrap]       – float left, text wraps right
    """
    text = text.replace(r"\n", "\n")

    def _replace(match: re.Match) -> str:
        path = match.group(1).strip()
        align = (match.group(2) or "center").strip()
        name = path.rsplit("/", 1)[-1]
        try:
            result = upload_func(project_id, issue_id, path)
        except Exception:
            return f'<p><em>[image upload failed: {path}]</em></p>'
        embed_url = result.get("embed_url") or result.get("asset_url") or ""
        if embed_url:
            if embed_url.startswith("/"):
                embed_url = base_url.rstrip("/") + embed_url
        else:
            return f'<p><em>[image URL unavailable: {path}]</em></p>'
        return _build_image_html(embed_url, align, name)

    text = _IMAGE_DIRECTIVE_RE.sub(_replace, text)

    try:
        import markdown
        return markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])
    except Exception:
        return f"<p>{text}</p>"

def append_images_to_html(
    html: str,
    uploaded_images: list[dict[str, Any]],
    base_url: str = "",
    align: str = "center",
) -> str:
    blocks: list[str] = []
    for image in uploaded_images:
        name = str(image.get("name") or "image")
        embed_url = image.get("embed_url") or image.get("asset_url")
        if embed_url:
            if embed_url.startswith("/"):
                embed_url = base_url.rstrip("/") + embed_url
            blocks.append(_build_image_html(embed_url, align, name))
        else:
            blocks.append(f'<p>已上传图片附件：{name}</p>')

    if not blocks:
        return html
    return f"{html}{''.join(blocks)}"


# ---------------------------------------------------------------------------
# Dataclasses & errors
# ---------------------------------------------------------------------------



@dataclass
class IssueSummary:
    id: str
    title: str
    state: str | None = None
    priority: str | None = None
    assignee: str | None = None
    project: str | None = None


class PlaneServiceError(RuntimeError):
    pass


class PlaneService:
    def __init__(self, client: PlaneClient, settings: Settings):
        self.client = client
        self.settings = settings

    # ----------------------------
    # Helpers
    # ----------------------------

    def _normalize(self, value: str | None) -> str:
        return (value or "").strip().lower()

    def _extract_name(
        self, obj: dict[str, Any], *keys: str
    ) -> str | None:
        for key in keys:
            value = obj.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return None

    def _find_by_name_or_id(
        self,
        items: list[dict[str, Any]],
        query: str,
        *,
        name_keys: tuple[str, ...] = ("name",),
    ) -> dict[str, Any] | None:
        q = self._normalize(query)

        # 1) exact id match
        for item in items:
            if self._normalize(str(item.get("id"))) == q:
                return item

        # 2) name / identifier match
        for item in items:
            for key in name_keys:
                if self._normalize(str(item.get(key))) == q:
                    return item

        return None

    # ----------------------------
    # Project resolution
    # ----------------------------

    def list_projects(self) -> list[dict[str, Any]]:
        return self.client.list_projects()

    def resolve_project(self, project_name_or_alias: str) -> dict[str, Any]:
        alias = self._normalize(project_name_or_alias)

        # alias -> actual project name
        mapped = self.settings.projects.get(alias, project_name_or_alias)

        projects = self.client.list_projects()
        project = self._find_by_name_or_id(
            projects,
            mapped,
            name_keys=("name", "identifier"),
        )

        if not project:
            raise PlaneServiceError(f"Project not found: {project_name_or_alias}")

        return project

    def get_default_project(self) -> dict[str, Any]:
        if not self.settings.default_project:
            raise PlaneServiceError("No default_project configured")
        return self.resolve_project(self.settings.default_project)

    # ----------------------------
    # State / label / member helpers
    # ----------------------------

    def list_states(
        self, project: str | None = None
    ) -> list[dict[str, Any]]:
        project_id = None
        if project:
            project_obj = self.resolve_project(project)
            project_id = str(project_obj["id"])

        return self.client.list_states(project_id=project_id)

    def list_labels(
        self, project: str | None = None
    ) -> list[dict[str, Any]]:
        project_id = None
        if project:
            project_obj = self.resolve_project(project)
            project_id = str(project_obj["id"])

        return self.client.list_labels(project_id=project_id)

    def list_members(self) -> list[dict[str, Any]]:
        return self.client.list_members()

    def resolve_state(
        self, target_state: str, project: str | None = None
    ) -> dict[str, Any]:
        mapped = self.settings.states.get(
            self._normalize(target_state), target_state
        )
        states = self.list_states(project=project)

        state = self._find_by_name_or_id(
            states, mapped, name_keys=("name",)
        )
        if not state:
            raise PlaneServiceError(f"State not found: {target_state}")

        return state

    # ----------------------------
    # Issues
    # ----------------------------

    def list_issues(
        self,
        project: str | None = None,
        state: str | None = None,
        assignee_id: str | None = None,
        priority: str | None = None,
        label_id: str | None = None,
        cycle_id: str | None = None,
    ) -> list[dict[str, Any]]:
        project_id = None
        state_id = None

        if project:
            project_obj = self.resolve_project(project)
            project_id = str(project_obj["id"])

        if state:
            state_obj = self.resolve_state(state, project=project)
            state_id = str(state_obj["id"])

        if priority:
            priority = self.settings.priorities.get(
                self._normalize(priority), priority
            )

        return self.client.list_issues(
            project_id=project_id,
            state_id=state_id,
            assignee_id=assignee_id,
            priority=priority,
            label_id=label_id,
            cycle_id=cycle_id,
        )

    def list_open_issues(
        self, project: str | None = None
    ) -> list[dict[str, Any]]:
        issues = self.list_issues(project=project)

        done_like = {"done", "completed", "closed", "canceled", "cancelled"}
        results: list[dict[str, Any]] = []

        for issue in issues:
            state_name = self._extract_state_name(issue)
            if self._normalize(state_name) not in done_like:
                results.append(issue)

        return results

    def list_high_priority_issues(
        self, project: str | None = None
    ) -> list[dict[str, Any]]:
        results = []
        issues = self.list_issues(project=project)

        for issue in issues:
            priority = self._normalize(str(issue.get("priority")))
            if priority in {"urgent", "high", "1", "2"}:
                results.append(issue)

        return results

    def get_issue_detail(
        self,
        issue_id: str,
        project: str | None = None,
    ) -> dict[str, Any]:
        if not project:
            raise PlaneServiceError(
                "get_issue_detail currently requires project"
            )
        project_obj = self.resolve_project(project)
        return self.client.get_issue(str(project_obj["id"]), issue_id)

    def create_issue(
        self,
        title: str,
        description: str,
        project: str | None = None,
        priority: str | None = None,
        state: str | None = None,
        extra_payload: dict[str, Any] | None = None,
        image_paths: list[str] | None = None,
        image_align: str = "center",
    ) -> dict[str, Any]:
        project_obj = (
            self.get_default_project()
            if not project
            else self.resolve_project(project)
        )
        payload: dict[str, Any] = {
            "name": title,
            "description_html": render_markdown(description),
        }

        if priority:
            payload["priority"] = self.settings.priorities.get(
                self._normalize(priority), priority
            )

        if state:
            state_obj = self.resolve_state(state, project=project_obj.get("name"))
            payload["state"] = state_obj["id"]

        if extra_payload:
            payload.update(extra_payload)

        issue = self.client.create_issue(str(project_obj["id"]), payload)

        # Resolve [image: path, align] directives in description before markdown
        description_html = payload["description_html"]
        if _IMAGE_DIRECTIVE_RE.search(description):
            description_html = render_markdown_with_inline_images(
                description,
                self.client.upload_attachment,
                str(project_obj["id"]),
                str(issue["id"]),
                self.client.base_url,
            )
            issue = self.client.update_issue(
                str(project_obj["id"]),
                str(issue["id"]),
                {"description_html": description_html},
            )

        if image_paths:
            uploaded_images: list[dict[str, Any]] = []
            for image_path in image_paths:
                uploaded_images.append(
                    self.client.upload_attachment(
                        str(project_obj["id"]),
                        str(issue["id"]),
                        image_path,
                    )
                )
            updated_html = append_images_to_html(
                str(issue.get("description_html") or description_html),
                uploaded_images,
                base_url=self.client.base_url,
                align=image_align,
            )
            issue = self.client.update_issue(
                str(project_obj["id"]),
                str(issue["id"]),
                {"description_html": updated_html},
            )

        return issue

    def update_issue_description(
        self,
        issue_id: str,
        description: str,
        project: str | None = None,
        image_paths: list[str] | None = None,
        image_align: str = "center",
    ) -> dict[str, Any]:
        if not project:
            raise PlaneServiceError(
                "update_issue_description currently requires project"
            )
        project_obj = self.resolve_project(project)
        # Resolve [image: path, align] directives before markdown
        if _IMAGE_DIRECTIVE_RE.search(description):
            base_html = render_markdown_with_inline_images(
                description,
                self.client.upload_attachment,
                str(project_obj["id"]),
                issue_id,
                self.client.base_url,
            )
        else:
            base_html = render_markdown(description)
        if image_paths:
            uploaded_images: list[dict[str, Any]] = []
            for image_path in image_paths:
                uploaded_images.append(
                    self.client.upload_attachment(
                        str(project_obj["id"]),
                        issue_id,
                        image_path,
                    )
                )
            base_html = append_images_to_html(
                base_html, uploaded_images,
                base_url=self.client.base_url,
                align=image_align,
            )
        payload = {
            "description_html": base_html,
        }
        return self.client.update_issue(str(project_obj["id"]), issue_id, payload)

    def move_issue(
        self,
        issue_id: str,
        target_state: str,
        project: str | None = None,
    ) -> dict[str, Any]:
        if not project:
            raise PlaneServiceError("move_issue currently requires project")

        project_obj = self.resolve_project(project)
        state_obj = self.resolve_state(target_state, project=project)

        payload = {
            "state": state_obj["id"],
        }
        return self.client.update_issue(str(project_obj["id"]), issue_id, payload)

    def assign_issue(
        self,
        issue_id: str,
        assignee: str,
        project: str | None = None,
    ) -> dict[str, Any]:
        if not project:
            raise PlaneServiceError("assign_issue currently requires project")

        project_obj = self.resolve_project(project)
        members = self.list_members()
        assignee_obj = self._find_member(members, assignee)
        if not assignee_obj:
            raise PlaneServiceError(f"Assignee not found: {assignee}")

        payload = {
            "assignees": [assignee_obj["id"]],
        }
        return self.client.update_issue(str(project_obj["id"]), issue_id, payload)

    def set_issue_priority(
        self,
        issue_id: str,
        priority: str,
        project: str | None = None,
    ) -> dict[str, Any]:
        if not project:
            raise PlaneServiceError("set_issue_priority currently requires project")

        project_obj = self.resolve_project(project)
        mapped = self.settings.priorities.get(self._normalize(priority), priority)
        payload = {
            "priority": mapped,
        }
        return self.client.update_issue(str(project_obj["id"]), issue_id, payload)

    def set_issue_labels(
        self,
        issue_id: str,
        labels: list[str],
        project: str | None = None,
    ) -> dict[str, Any]:
        if not project:
            raise PlaneServiceError("set_issue_labels currently requires project")

        project_obj = self.resolve_project(project)
        label_objs = self.list_labels(project=project)
        label_ids: list[str] = []
        for label in labels:
            obj = self._find_by_name_or_id(label_objs, label, name_keys=("name",))
            if not obj:
                raise PlaneServiceError(f"Label not found: {label}")
            label_ids.append(str(obj["id"]))

        payload = {
            "labels": label_ids,
        }
        return self.client.update_issue(str(project_obj["id"]), issue_id, payload)

    def upload_attachment(
        self,
        issue_id: str,
        file_path: str,
        project: str | None = None,
    ) -> dict[str, Any]:
        if not project:
            raise PlaneServiceError("upload_attachment requires project")
        project_obj = self.resolve_project(project)
        result = self.client.upload_attachment(
            str(project_obj["id"]),
            issue_id,
            file_path,
        )
        return result

    def list_cycles(self, project: str) -> list[dict[str, Any]]:
        project_obj = self.resolve_project(project)
        return self.client.list_cycles(str(project_obj["id"]))

    def get_cycle_detail(
        self, project: str, cycle_id: str
    ) -> dict[str, Any]:
        project_obj = self.resolve_project(project)
        return self.client.get_cycle(str(project_obj["id"]), cycle_id)

    def create_cycle(
        self,
        project: str,
        name: str,
        description: str = "",
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        project_obj = self.resolve_project(project)
        return self.client.create_cycle(
            str(project_obj["id"]),
            name,
            description,
            start_date,
            end_date,
        )

    def add_issues_to_cycle(
        self,
        project: str,
        cycle_id: str,
        issue_ids: list[str],
    ) -> list[dict[str, Any]]:
        project_obj = self.resolve_project(project)
        return self.client.add_issues_to_cycle(
            str(project_obj["id"]), cycle_id, issue_ids
        )

    def remove_issue_from_cycle(
        self,
        project: str,
        cycle_id: str,
        issue_id: str,
    ) -> None:
        project_obj = self.resolve_project(project)
        self.client.remove_issue_from_cycle(
            str(project_obj["id"]), cycle_id, issue_id
        )

    def list_comments(
        self, issue_id: str, project: str | None = None
    ) -> list[dict[str, Any]]:
        if not project:
            raise PlaneServiceError("list_comments requires project")
        project_obj = self.resolve_project(project)
        return self.client.list_comments(
            str(project_obj["id"]), issue_id
        )

    def create_comment(
        self,
        issue_id: str,
        content: str,
        project: str | None = None,
        image_paths: list[str] | None = None,
        image_align: str = "center",
    ) -> dict[str, Any]:
        if not project:
            raise PlaneServiceError("create_comment requires project")
        project_obj = self.resolve_project(project)
        html = render_markdown(content)
        if image_paths:
            uploaded_images: list[dict[str, Any]] = []
            for image_path in image_paths:
                uploaded_images.append(
                    self.client.upload_attachment(
                        str(project_obj["id"]),
                        issue_id,
                        image_path,
                    )
                )
            html = append_images_to_html(
                html, uploaded_images,
                base_url=self.client.base_url,
                align=image_align,
            )
        return self.client.create_comment(
            str(project_obj["id"]), issue_id, html
        )

    def add_issue_link(
        self,
        issue_id: str,
        url: str,
        title: str = "",
        project: str | None = None,
    ) -> dict[str, Any]:
        if not project:
            raise PlaneServiceError("add_issue_link requires project")
        project_obj = self.resolve_project(project)
        return self.client.create_issue_link(
            str(project_obj["id"]), issue_id, url, title
        )

    def create_project(
        self, name: str, identifier: str, description: str = ""
    ) -> dict[str, Any]:
        return self.client.create_project(name, identifier, description)

    # ----------------------------
    # Summaries
    # ----------------------------

    def summarize_issue(self, issue: dict[str, Any]) -> IssueSummary:
        return IssueSummary(
            id=str(issue.get("id", "")),
            title=str(issue.get("name") or issue.get("title") or ""),
            state=self._extract_state_name(issue),
            priority=issue.get("priority"),
            assignee=self._extract_assignee_name(issue),
            project=self._extract_project_name(issue),
        )

    def summarize_project(self, project: str) -> dict[str, Any]:
        issues = self.list_issues(project=project)
        state_map = self.get_state_id_name_map(project)

        state_counter: dict[str, int] = {}
        open_issues = 0
        high_priority_open_issues = 0
        done_like = {"done", "completed", "closed", "canceled", "cancelled"}

        for issue in issues:
            state_name = self._extract_state_name(issue, state_map=state_map) or "unknown"
            priority = self._normalize(str(issue.get("priority")))

            state_counter[state_name] = state_counter.get(state_name, 0) + 1

            if self._normalize(state_name) not in done_like:
                open_issues += 1
                if priority in {"urgent", "high", "1", "2"}:
                    high_priority_open_issues += 1

        return {
            "project": project,
            "total_issues": len(issues),
            "open_issues": open_issues,
            "high_priority_open_issues": high_priority_open_issues,
            "by_state": state_counter,
        }

    # ----------------------------
    # Extraction helpers
    # ----------------------------

    def get_state_id_name_map(self, project: str | None = None) -> dict[str, str]:
        states = self.list_states(project=project)
        mapping: dict[str, str] = {}
        for state in states:
            sid = state.get("id")
            name = state.get("name")
            if sid and name:
                mapping[str(sid)] = str(name)
        return mapping

    def _extract_state_name(
        self,
        issue: dict[str, Any],
        state_map: dict[str, str] | None = None,
    ) -> str | None:
        state = issue.get("state")
        if isinstance(state, dict):
            return self._extract_name(state, "name")
        if isinstance(state, str):
            if state_map and state in state_map:
                return state_map[state]
            return state
        return None

    def _extract_project_name(self, issue: dict[str, Any]) -> str | None:
        proj = issue.get("project")
        if isinstance(proj, dict):
            return self._extract_name(proj, "name", "identifier")
        if isinstance(proj, str):
            return proj
        return None

    def _extract_assignee_name(self, issue: dict[str, Any]) -> str | None:
        assignee = issue.get("assignee")
        if isinstance(assignee, dict):
            return self._extract_name(
                assignee, "display_name", "name", "email"
            )

        assignees = issue.get("assignees")
        if isinstance(assignees, list) and assignees:
            first = assignees[0]
            if isinstance(first, dict):
                return self._extract_name(
                    first, "display_name", "name", "email"
                )

        if isinstance(assignee, list) and assignee:
            first = assignee[0]
            if isinstance(first, dict):
                return self._extract_name(
                    first, "display_name", "name", "email"
                )
        return None

    def _find_member(
        self,
        members: list[dict[str, Any]],
        query: str,
    ) -> dict[str, Any] | None:
        q = self._normalize(query)
        for item in members:
            member = item.get("member") if isinstance(item.get("member"), dict) else item
            mid = self._normalize(str(member.get("id")))
            name = self._normalize(str(member.get("display_name") or member.get("name")))
            email = self._normalize(str(member.get("email")))
            if q in {mid, name, email}:
                return member
        return None
