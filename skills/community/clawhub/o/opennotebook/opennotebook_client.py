#!/usr/bin/env python3
"""
OpenNotebook API Client

A comprehensive Python client for interacting with OpenNotebook API.
Supports all endpoints for notebooks, sources, notes, insights, models,
transformations, chat, podcasts, and credentials management.

Configuration:
    - OPENNOTEBOOK_BASE_URL: Base URL for the API (default: http://localhost:8000)
    - OPENNOTEBOOK_API_KEY: API key for authentication (optional)

Usage:
    from opennotebook_client import OpenNotebookClient

    client = OpenNotebookClient(base_url="http://localhost:8000")

    # List notebooks
    notebooks = client.notebooks.list()

    # Create a notebook
    notebook = client.notebooks.create(name="My Notebook", description="Description")

    # Search
    results = client.search.query("machine learning")
"""

import os
import json
import requests
from typing import Optional, Dict, List, Any, Union
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    """Configuration for the OpenNotebook client."""
    base_url: str = field(default_factory=lambda: os.getenv("OPENNOTEBOOK_BASE_URL", "http://localhost:8000"))
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENNOTEBOOK_API_KEY"))
    timeout: int = 30
    verify_ssl: bool = True


class OpenNotebookError(Exception):
    """Base exception for OpenNotebook API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class BaseClient:
    """Base client with common HTTP methods."""

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def _request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{self.config.base_url.rstrip('/')}{path}"
        headers = self._headers()

        # Handle multipart form data
        if "files" in kwargs:
            headers.pop("Content-Type", None)

        kwargs.setdefault("timeout", self.config.timeout)
        kwargs.setdefault("verify", self.config.verify_ssl)

        response = self.session.request(method, url, headers=headers, **kwargs)

        if response.status_code >= 400:
            try:
                error_data = response.json()
            except:
                error_data = {"detail": response.text}
            raise OpenNotebookError(
                f"API Error: {response.status_code} - {error_data}",
                status_code=response.status_code,
                response=error_data
            )

        if response.status_code == 204:
            return None

        try:
            return response.json()
        except:
            return response.content

    def _get(self, path: str, params: Optional[Dict] = None) -> Any:
        return self._request("GET", path, params=params)

    def _post(self, path: str, data: Optional[Dict] = None, files: Optional[Dict] = None) -> Any:
        if files:
            return self._request("POST", path, data=data, files=files)
        return self._request("POST", path, json=data)

    def _put(self, path: str, data: Optional[Dict] = None) -> Any:
        return self._request("PUT", path, json=data)

    def _delete(self, path: str, params: Optional[Dict] = None) -> Any:
        return self._request("DELETE", path, params=params)


class AuthClient(BaseClient):
    """Client for authentication endpoints."""

    def status(self) -> Dict:
        """Get authentication status."""
        return self._get("/api/auth/status")


class ConfigClient(BaseClient):
    """Client for configuration endpoints."""

    def get(self) -> Dict:
        """Get application configuration."""
        return self._get("/api/config")


class NotebooksClient(BaseClient):
    """Client for notebook operations."""

    def list(self, archived: Optional[bool] = None, order_by: Optional[str] = None) -> List[Dict]:
        """List all notebooks.

        Args:
            archived: Filter by archived status
            order_by: Field to order by
        """
        params = {}
        if archived is not None:
            params["archived"] = archived
        if order_by:
            params["order_by"] = order_by
        return self._get("/api/notebooks", params=params)

    def get(self, notebook_id: str) -> Dict:
        """Get a specific notebook."""
        return self._get(f"/api/notebooks/{notebook_id}")

    def create(self, name: str, description: Optional[str] = None) -> Dict:
        """Create a new notebook."""
        data = {"name": name}
        if description:
            data["description"] = description
        return self._post("/api/notebooks", data=data)

    def update(self, notebook_id: str, name: Optional[str] = None,
               description: Optional[str] = None, archived: Optional[bool] = None) -> Dict:
        """Update a notebook."""
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if archived is not None:
            data["archived"] = archived
        return self._put(f"/api/notebooks/{notebook_id}", data=data)

    def delete(self, notebook_id: str, delete_exclusive_sources: bool = False) -> None:
        """Delete a notebook.

        Args:
            notebook_id: Notebook ID
            delete_exclusive_sources: Also delete sources only in this notebook
        """
        params = {"delete_exclusive_sources": delete_exclusive_sources}
        return self._delete(f"/api/notebooks/{notebook_id}", params=params)

    def delete_preview(self, notebook_id: str) -> Dict:
        """Preview what will be deleted when deleting a notebook."""
        return self._get(f"/api/notebooks/{notebook_id}/delete-preview")

    def add_source(self, notebook_id: str, source_id: str) -> Dict:
        """Add a source to a notebook."""
        return self._post(f"/api/notebooks/{notebook_id}/sources/{source_id}")

    def remove_source(self, notebook_id: str, source_id: str) -> None:
        """Remove a source from a notebook."""
        return self._delete(f"/api/notebooks/{notebook_id}/sources/{source_id}")

    def get_context(self, notebook_id: str, context_config: Optional[Dict] = None) -> Dict:
        """Get notebook context for AI processing."""
        data = {"notebook_id": notebook_id}
        if context_config:
            data["context_config"] = context_config
        return self._post(f"/api/notebooks/{notebook_id}/context", data=data)


class SearchClient(BaseClient):
    """Client for search operations."""

    def query(self, query: str, type: Optional[str] = None, limit: Optional[int] = None,
              search_sources: bool = True, search_notes: bool = True,
              minimum_score: Optional[float] = None) -> Dict:
        """Search the knowledge base.

        Args:
            query: Search query string
            type: Type of search
            limit: Maximum results
            search_sources: Include sources in search
            search_notes: Include notes in search
            minimum_score: Minimum relevance score
        """
        data = {"query": query}
        if type:
            data["type"] = type
        if limit:
            data["limit"] = limit
        data["search_sources"] = search_sources
        data["search_notes"] = search_notes
        if minimum_score:
            data["minimum_score"] = minimum_score
        return self._post("/api/search", data=data)

    def ask(self, question: str, strategy_model: str, answer_model: str,
            final_answer_model: str) -> Dict:
        """Ask a question using AI models.

        Args:
            question: The question to ask
            strategy_model: Model for strategy planning
            answer_model: Model for answering
            final_answer_model: Model for final answer synthesis
        """
        data = {
            "question": question,
            "strategy_model": strategy_model,
            "answer_model": answer_model,
            "final_answer_model": final_answer_model
        }
        return self._post("/api/search/ask", data=data)

    def ask_simple(self, question: str, strategy_model: str, answer_model: str,
                   final_answer_model: str) -> Dict:
        """Simple ask endpoint (streaming not included)."""
        data = {
            "question": question,
            "strategy_model": strategy_model,
            "answer_model": answer_model,
            "final_answer_model": final_answer_model
        }
        return self._post("/api/search/ask/simple", data=data)


class ModelsClient(BaseClient):
    """Client for model management."""

    def list(self, type: Optional[str] = None) -> List[Dict]:
        """List available models."""
        params = {}
        if type:
            params["type"] = type
        return self._get("/api/models", params=params)

    def get(self, model_id: str) -> Dict:
        """Get a specific model."""
        return self._get(f"/api/models/{model_id}")

    def create(self, name: str, provider: str, type: str, credential: Optional[str] = None) -> Dict:
        """Create a new model configuration."""
        data = {"name": name, "provider": provider, "type": type}
        if credential:
            data["credential"] = credential
        return self._post("/api/models", data=data)

    def delete(self, model_id: str) -> None:
        """Delete a model."""
        return self._delete(f"/api/models/{model_id}")

    def test(self, model_id: str) -> Dict:
        """Test a model connection."""
        return self._post(f"/api/models/{model_id}/test")

    def get_defaults(self) -> Dict:
        """Get default model assignments."""
        return self._get("/api/models/defaults")

    def update_defaults(self, defaults: Dict) -> Dict:
        """Update default model assignments."""
        return self._put("/api/models/defaults", data=defaults)

    def get_providers(self) -> List[str]:
        """Get list of available providers."""
        return self._get("/api/models/providers")

    def discover(self, provider: str) -> List[Dict]:
        """Discover models for a provider."""
        return self._get(f"/api/models/discover/{provider}")

    def sync(self, provider: Optional[str] = None) -> Dict:
        """Sync models from provider(s)."""
        if provider:
            return self._post(f"/api/models/sync/{provider}")
        return self._post("/api/models/sync")

    def count(self, provider: str) -> int:
        """Get count of models for a provider."""
        return self._get(f"/api/models/count/{provider}")

    def by_provider(self, provider: str) -> List[Dict]:
        """Get models by provider."""
        return self._get(f"/api/models/by-provider/{provider}")

    def auto_assign_defaults(self) -> Dict:
        """Auto-assign default models."""
        return self._post("/api/models/auto-assign")


class TransformationsClient(BaseClient):
    """Client for transformation operations."""

    def list(self) -> List[Dict]:
        """List all transformations."""
        return self._get("/api/transformations")

    def get(self, transformation_id: str) -> Dict:
        """Get a specific transformation."""
        return self._get(f"/api/transformations/{transformation_id}")

    def create(self, name: str, title: str, description: str, prompt: str,
               apply_default: bool = False) -> Dict:
        """Create a new transformation."""
        data = {
            "name": name,
            "title": title,
            "description": description,
            "prompt": prompt,
            "apply_default": apply_default
        }
        return self._post("/api/transformations", data=data)

    def update(self, transformation_id: str, **kwargs) -> Dict:
        """Update a transformation."""
        return self._put(f"/api/transformations/{transformation_id}", data=kwargs)

    def delete(self, transformation_id: str) -> None:
        """Delete a transformation."""
        return self._delete(f"/api/transformations/{transformation_id}")

    def execute(self, transformation_id: str, input_text: str, model_id: str) -> Dict:
        """Execute a transformation."""
        data = {
            "transformation_id": transformation_id,
            "input_text": input_text,
            "model_id": model_id
        }
        return self._post("/api/transformations/execute", data=data)

    def get_default_prompt(self) -> Dict:
        """Get default transformation prompt."""
        return self._get("/api/transformations/default-prompt")

    def update_default_prompt(self, transformation_instructions: str) -> Dict:
        """Update default transformation prompt."""
        return self._put("/api/transformations/default-prompt",
                        data={"transformation_instructions": transformation_instructions})


class NotesClient(BaseClient):
    """Client for note operations."""

    def list(self, notebook_id: Optional[str] = None) -> List[Dict]:
        """List notes, optionally filtered by notebook."""
        params = {}
        if notebook_id:
            params["notebook_id"] = notebook_id
        return self._get("/api/notes", params=params)

    def get(self, note_id: str) -> Dict:
        """Get a specific note."""
        return self._get(f"/api/notes/{note_id}")

    def create(self, content: str, title: Optional[str] = None,
               note_type: Optional[str] = None, notebook_id: Optional[str] = None) -> Dict:
        """Create a new note."""
        data = {"content": content}
        if title:
            data["title"] = title
        if note_type:
            data["note_type"] = note_type
        if notebook_id:
            data["notebook_id"] = notebook_id
        return self._post("/api/notes", data=data)

    def update(self, note_id: str, **kwargs) -> Dict:
        """Update a note."""
        return self._put(f"/api/notes/{note_id}", data=kwargs)

    def delete(self, note_id: str) -> None:
        """Delete a note."""
        return self._delete(f"/api/notes/{note_id}")


class EmbeddingsClient(BaseClient):
    """Client for embedding operations."""

    def embed(self, item_id: str, item_type: str, async_processing: bool = True) -> Dict:
        """Embed content.

        Args:
            item_id: ID of the item to embed
            item_type: Type of item (source, note, insight)
            async_processing: Process asynchronously
        """
        data = {
            "item_id": item_id,
            "item_type": item_type,
            "async_processing": async_processing
        }
        return self._post("/api/embed", data=data)

    def rebuild(self, mode: str, include_sources: bool = True,
                include_notes: bool = True, include_insights: bool = True) -> Dict:
        """Rebuild embeddings.

        Args:
            mode: Rebuild mode (full, incremental)
            include_sources: Include sources
            include_notes: Include notes
            include_insights: Include insights
        """
        data = {
            "mode": mode,
            "include_sources": include_sources,
            "include_notes": include_notes,
            "include_insights": include_insights
        }
        return self._post("/api/embeddings/rebuild", data=data)

    def rebuild_status(self, command_id: str) -> Dict:
        """Get rebuild status."""
        return self._get(f"/api/embeddings/rebuild/{command_id}/status")


class SourcesClient(BaseClient):
    """Client for source operations."""

    def list(self, notebook_id: Optional[str] = None, limit: int = 50,
             offset: int = 0, sort_by: str = "created",
             sort_order: str = "desc") -> Dict:
        """List sources with pagination."""
        params = {"limit": limit, "offset": offset, "sort_by": sort_by, "sort_order": sort_order}
        if notebook_id:
            params["notebook_id"] = notebook_id
        return self._get("/api/sources", params=params)

    def get(self, source_id: str) -> Dict:
        """Get a specific source."""
        return self._get(f"/api/sources/{source_id}")

    def create(self, type: str, notebook_id: Optional[str] = None,
               url: Optional[str] = None, content: Optional[str] = None,
               title: Optional[str] = None, transformations: Optional[List[str]] = None,
               embed: bool = True, async_processing: bool = True) -> Dict:
        """Create a source (JSON API).

        Args:
            type: Source type (file, url, text, youtube, etc.)
            notebook_id: Notebook to add source to
            url: URL for url/youtube types
            content: Content for text type
            title: Optional title
            transformations: List of transformation IDs to apply
            embed: Whether to create embeddings
            async_processing: Process asynchronously
        """
        data = {"type": type}
        if notebook_id:
            data["notebook_id"] = notebook_id
        if url:
            data["url"] = url
        if content:
            data["content"] = content
        if title:
            data["title"] = title
        if transformations:
            data["transformations"] = transformations
        data["embed"] = embed
        data["async_processing"] = async_processing
        return self._post("/api/sources/json", data=data)

    def upload(self, file_path: str, notebook_id: Optional[str] = None,
               title: Optional[str] = None, transformations: Optional[List[str]] = None,
               embed: bool = True) -> Dict:
        """Upload a file as a source.

        Args:
            file_path: Path to the file to upload
            notebook_id: Notebook to add source to
            title: Optional title
            transformations: List of transformation IDs
            embed: Whether to create embeddings
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        data = {}
        if notebook_id:
            data["notebook_id"] = notebook_id
        if title:
            data["title"] = title
        if transformations:
            data["transformations"] = json.dumps(transformations)
        data["embed"] = str(embed).lower()

        with open(path, "rb") as f:
            files = {"file": (path.name, f)}
            return self._post("/api/sources", data=data, files=files)

    def update(self, source_id: str, title: Optional[str] = None,
               topics: Optional[List[str]] = None) -> Dict:
        """Update a source."""
        data = {}
        if title:
            data["title"] = title
        if topics:
            data["topics"] = topics
        return self._put(f"/api/sources/{source_id}", data=data)

    def delete(self, source_id: str) -> None:
        """Delete a source."""
        return self._delete(f"/api/sources/{source_id}")

    def download(self, source_id: str) -> bytes:
        """Download source file content."""
        return self._get(f"/api/sources/{source_id}/download")

    def status(self, source_id: str) -> Dict:
        """Get source processing status."""
        return self._get(f"/api/sources/{source_id}/status")

    def retry(self, source_id: str) -> Dict:
        """Retry source processing."""
        return self._post(f"/api/sources/{source_id}/retry")

    def get_insights(self, source_id: str) -> List[Dict]:
        """Get insights for a source."""
        return self._get(f"/api/sources/{source_id}/insights")

    def create_insight(self, source_id: str, transformation_id: str,
                       model_id: Optional[str] = None) -> Dict:
        """Create an insight for a source."""
        data = {"transformation_id": transformation_id}
        if model_id:
            data["model_id"] = model_id
        return self._post(f"/api/sources/{source_id}/insights", data=data)


class InsightsClient(BaseClient):
    """Client for insight operations."""

    def get(self, insight_id: str) -> Dict:
        """Get a specific insight."""
        return self._get(f"/api/insights/{insight_id}")

    def delete(self, insight_id: str) -> None:
        """Delete an insight."""
        return self._delete(f"/api/insights/{insight_id}")

    def save_as_note(self, insight_id: str, notebook_id: Optional[str] = None) -> Dict:
        """Save an insight as a note."""
        data = {}
        if notebook_id:
            data["notebook_id"] = notebook_id
        return self._post(f"/api/insights/{insight_id}/save-as-note", data=data)


class ChatClient(BaseClient):
    """Client for chat operations."""

    def list_sessions(self) -> List[Dict]:
        """List all chat sessions."""
        return self._get("/api/chat/sessions")

    def get_session(self, session_id: str) -> Dict:
        """Get a chat session."""
        return self._get(f"/api/chat/sessions/{session_id}")

    def create_session(self, **kwargs) -> Dict:
        """Create a new chat session."""
        return self._post("/api/chat/sessions", data=kwargs)

    def update_session(self, session_id: str, **kwargs) -> Dict:
        """Update a chat session."""
        return self._put(f"/api/chat/sessions/{session_id}", data=kwargs)

    def delete_session(self, session_id: str) -> None:
        """Delete a chat session."""
        return self._delete(f"/api/chat/sessions/{session_id}")

    def execute(self, **kwargs) -> Dict:
        """Execute a chat query."""
        return self._post("/api/chat/execute", data=kwargs)

    def get_context(self, **kwargs) -> Dict:
        """Get chat context."""
        return self._post("/api/chat/context", data=kwargs)

    # Source-specific chat sessions
    def list_source_sessions(self, source_id: str) -> List[Dict]:
        """List chat sessions for a source."""
        return self._get(f"/api/sources/{source_id}/chat/sessions")

    def create_source_session(self, source_id: str, **kwargs) -> Dict:
        """Create a chat session for a source."""
        return self._post(f"/api/sources/{source_id}/chat/sessions", data=kwargs)

    def get_source_session(self, source_id: str, session_id: str) -> Dict:
        """Get a source chat session."""
        return self._get(f"/api/sources/{source_id}/chat/sessions/{session_id}")

    def update_source_session(self, source_id: str, session_id: str, **kwargs) -> Dict:
        """Update a source chat session."""
        return self._put(f"/api/sources/{source_id}/chat/sessions/{session_id}", data=kwargs)

    def delete_source_session(self, source_id: str, session_id: str) -> None:
        """Delete a source chat session."""
        return self._delete(f"/api/sources/{source_id}/chat/sessions/{session_id}")

    def add_message(self, source_id: str, session_id: str, **kwargs) -> Dict:
        """Add a message to a source chat session."""
        return self._post(f"/api/sources/{source_id}/chat/sessions/{session_id}/messages", data=kwargs)


class PodcastsClient(BaseClient):
    """Client for podcast operations."""

    def generate(self, **kwargs) -> Dict:
        """Generate a podcast."""
        return self._post("/api/podcasts/generate", data=kwargs)

    def get_job(self, job_id: str) -> Dict:
        """Get podcast generation job status."""
        return self._get(f"/api/podcasts/jobs/{job_id}")

    def list_episodes(self) -> List[Dict]:
        """List all podcast episodes."""
        return self._get("/api/podcasts/episodes")

    def get_episode(self, episode_id: str) -> Dict:
        """Get a podcast episode."""
        return self._get(f"/api/podcasts/episodes/{episode_id}")

    def delete_episode(self, episode_id: str) -> None:
        """Delete a podcast episode."""
        return self._delete(f"/api/podcasts/episodes/{episode_id}")

    def get_episode_audio(self, episode_id: str) -> bytes:
        """Get podcast episode audio."""
        return self._get(f"/api/podcasts/episodes/{episode_id}/audio")

    def retry_episode(self, episode_id: str) -> Dict:
        """Retry podcast episode generation."""
        return self._post(f"/api/podcasts/episodes/{episode_id}/retry")


class EpisodeProfilesClient(BaseClient):
    """Client for episode profile operations."""

    def list(self) -> List[Dict]:
        """List all episode profiles."""
        return self._get("/api/episode-profiles")

    def get(self, profile_id: str) -> Dict:
        """Get an episode profile."""
        return self._get(f"/api/episode-profiles/{profile_id}")

    def get_by_name(self, profile_name: str) -> Dict:
        """Get an episode profile by name."""
        return self._get(f"/api/episode-profiles/{profile_name}")

    def create(self, **kwargs) -> Dict:
        """Create an episode profile."""
        return self._post("/api/episode-profiles", data=kwargs)

    def update(self, profile_id: str, **kwargs) -> Dict:
        """Update an episode profile."""
        return self._put(f"/api/episode-profiles/{profile_id}", data=kwargs)

    def delete(self, profile_id: str) -> None:
        """Delete an episode profile."""
        return self._delete(f"/api/episode-profiles/{profile_id}")

    def duplicate(self, profile_id: str) -> Dict:
        """Duplicate an episode profile."""
        return self._post(f"/api/episode-profiles/{profile_id}/duplicate")


class SpeakerProfilesClient(BaseClient):
    """Client for speaker profile operations."""

    def list(self) -> List[Dict]:
        """List all speaker profiles."""
        return self._get("/api/speaker-profiles")

    def get(self, profile_id: str) -> Dict:
        """Get a speaker profile."""
        return self._get(f"/api/speaker-profiles/{profile_id}")

    def get_by_name(self, profile_name: str) -> Dict:
        """Get a speaker profile by name."""
        return self._get(f"/api/speaker-profiles/{profile_name}")

    def create(self, **kwargs) -> Dict:
        """Create a speaker profile."""
        return self._post("/api/speaker-profiles", data=kwargs)

    def update(self, profile_id: str, **kwargs) -> Dict:
        """Update a speaker profile."""
        return self._put(f"/api/speaker-profiles/{profile_id}", data=kwargs)

    def delete(self, profile_id: str) -> None:
        """Delete a speaker profile."""
        return self._delete(f"/api/speaker-profiles/{profile_id}")

    def duplicate(self, profile_id: str) -> Dict:
        """Duplicate a speaker profile."""
        return self._post(f"/api/speaker-profiles/{profile_id}/duplicate")


class CredentialsClient(BaseClient):
    """Client for credential management."""

    def status(self) -> Dict:
        """Get credentials status."""
        return self._get("/api/credentials/status")

    def env_status(self) -> Dict:
        """Get environment credentials status."""
        return self._get("/api/credentials/env-status")

    def list(self) -> List[Dict]:
        """List all credentials."""
        return self._get("/api/credentials")

    def get(self, credential_id: str) -> Dict:
        """Get a credential."""
        return self._get(f"/api/credentials/{credential_id}")

    def create(self, **kwargs) -> Dict:
        """Create a credential."""
        return self._post("/api/credentials", data=kwargs)

    def update(self, credential_id: str, **kwargs) -> Dict:
        """Update a credential."""
        return self._put(f"/api/credentials/{credential_id}", data=kwargs)

    def delete(self, credential_id: str) -> None:
        """Delete a credential."""
        return self._delete(f"/api/credentials/{credential_id}")

    def test(self, credential_id: str) -> Dict:
        """Test a credential."""
        return self._post(f"/api/credentials/{credential_id}/test")

    def discover(self, credential_id: str) -> Dict:
        """Discover models using a credential."""
        return self._post(f"/api/credentials/{credential_id}/discover")

    def register_models(self, credential_id: str) -> Dict:
        """Register models for a credential."""
        return self._post(f"/api/credentials/{credential_id}/register-models")

    def by_provider(self, provider: str) -> List[Dict]:
        """Get credentials by provider."""
        return self._get(f"/api/credentials/by-provider/{provider}")

    def migrate_from_provider_config(self) -> Dict:
        """Migrate from provider config."""
        return self._post("/api/credentials/migrate-from-provider-config")

    def migrate_from_env(self) -> Dict:
        """Migrate credentials from environment."""
        return self._post("/api/credentials/migrate-from-env")


class CommandsClient(BaseClient):
    """Client for command/job operations."""

    def list_jobs(self) -> List[Dict]:
        """List all jobs."""
        return self._get("/api/commands/jobs")

    def create_job(self, **kwargs) -> Dict:
        """Create a job."""
        return self._post("/api/commands/jobs", data=kwargs)

    def get_job(self, job_id: str) -> Dict:
        """Get a job."""
        return self._get(f"/api/commands/jobs/{job_id}")

    def delete_job(self, job_id: str) -> None:
        """Delete a job."""
        return self._delete(f"/api/commands/jobs/{job_id}")

    def debug_registry(self) -> Dict:
        """Debug the command registry."""
        return self._get("/api/commands/registry/debug")


class SettingsClient(BaseClient):
    """Client for settings operations."""

    def get(self) -> Dict:
        """Get all settings."""
        return self._get("/api/settings")

    def update(self, **kwargs) -> Dict:
        """Update settings."""
        return self._put("/api/settings", data=kwargs)


class LanguagesClient(BaseClient):
    """Client for language operations."""

    def list(self) -> List[Dict]:
        """Get supported languages."""
        return self._get("/api/languages")


class OpenNotebookClient:
    """
    Main client for OpenNotebook API.

    Provides access to all API endpoints through specialized sub-clients.

    Usage:
        client = OpenNotebookClient(base_url="http://localhost:8000")

        # Notebooks
        notebooks = client.notebooks.list()
        notebook = client.notebooks.create(name="Research")

        # Sources
        source = client.sources.create(type="url", url="https://example.com")
        client.sources.upload("/path/to/file.pdf")

        # Search
        results = client.search.query("machine learning")
        answer = client.search.ask(question="What is AI?", ...)

        # Chat
        session = client.chat.create_session()
        response = client.chat.execute(session_id=session["id"], message="Hello")
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None,
                 timeout: int = 30, verify_ssl: bool = True):
        """
        Initialize the OpenNotebook client.

        Args:
            base_url: API base URL (default: from OPENNOTEBOOK_BASE_URL env or http://localhost:8000)
            api_key: API key (default: from OPENNOTEBOOK_API_KEY env)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        config = Config(
            base_url=base_url or os.getenv("OPENNOTEBOOK_BASE_URL", "http://localhost:8000"),
            api_key=api_key or os.getenv("OPENNOTEBOOK_API_KEY"),
            timeout=timeout,
            verify_ssl=verify_ssl
        )

        # Initialize sub-clients
        self.auth = AuthClient(config)
        self.config = ConfigClient(config)
        self.notebooks = NotebooksClient(config)
        self.search = SearchClient(config)
        self.models = ModelsClient(config)
        self.transformations = TransformationsClient(config)
        self.notes = NotesClient(config)
        self.embeddings = EmbeddingsClient(config)
        self.sources = SourcesClient(config)
        self.insights = InsightsClient(config)
        self.chat = ChatClient(config)
        self.podcasts = PodcastsClient(config)
        self.episode_profiles = EpisodeProfilesClient(config)
        self.speaker_profiles = SpeakerProfilesClient(config)
        self.credentials = CredentialsClient(config)
        self.commands = CommandsClient(config)
        self.settings = SettingsClient(config)
        self.languages = LanguagesClient(config)

    def health(self) -> Dict:
        """Check API health."""
        return self._get("/health")

    def _get(self, path: str) -> Any:
        """Direct GET request."""
        config = self.notebooks.config
        return BaseClient(config)._get(path)


# CLI interface for quick testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OpenNotebook API Client")
    parser.add_argument("--base-url", default=os.getenv("OPENNOTEBOOK_BASE_URL", "http://localhost:8000"))
    parser.add_argument("--api-key", default=os.getenv("OPENNOTEBOOK_API_KEY"))
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Notebooks
    nb_parser = subparsers.add_parser("notebooks", help="Notebook operations")
    nb_parser.add_argument("action", choices=["list", "create", "get", "delete"])
    nb_parser.add_argument("--name", help="Notebook name")
    nb_parser.add_argument("--id", help="Notebook ID")

    # Sources
    src_parser = subparsers.add_parser("sources", help="Source operations")
    src_parser.add_argument("action", choices=["list", "upload", "create"])
    src_parser.add_argument("--file", help="File to upload")
    src_parser.add_argument("--url", help="URL to add")
    src_parser.add_argument("--type", help="Source type")

    # Search
    search_parser = subparsers.add_parser("search", help="Search operations")
    search_parser.add_argument("query", help="Search query")

    # Health
    subparsers.add_parser("health", help="Check API health")

    args = parser.parse_args()

    client = OpenNotebookClient(base_url=args.base_url, api_key=args.api_key)

    if args.command == "health":
        print(json.dumps(client.health(), indent=2))
    elif args.command == "notebooks":
        if args.action == "list":
            print(json.dumps(client.notebooks.list(), indent=2))
        elif args.action == "create" and args.name:
            print(json.dumps(client.notebooks.create(name=args.name), indent=2))
        elif args.action == "get" and args.id:
            print(json.dumps(client.notebooks.get(args.id), indent=2))
    elif args.command == "sources":
        if args.action == "list":
            print(json.dumps(client.sources.list(), indent=2))
        elif args.action == "upload" and args.file:
            print(json.dumps(client.sources.upload(args.file), indent=2))
    elif args.command == "search":
        print(json.dumps(client.search.query(args.query), indent=2))
    else:
        parser.print_help()