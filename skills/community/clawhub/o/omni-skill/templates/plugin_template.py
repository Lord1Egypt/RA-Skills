from src.core.interfaces import OmniPlugin
from typing import Dict, Any

class TemplatePlugin(OmniPlugin):
    """
    Template for creating a new OmniSkill Plugin.
    Replace 'TemplatePlugin' and 'name' with your plugin's identity.
    """
    name = "my_plugin_name"
    version = "1.0.0"
    dependencies = [] # Add names of plugins this one depends on

    def on_init(self, config: Dict[str, Any]) -> None:
        """Called once during registration."""
        self.config = config
        self.db_connection = None
        print(f"[{self.name}] Initialized with config: {config}")

    def on_start(self) -> None:
        """Called when the OmniSkill Kernel starts."""
        print(f"[{self.name}] Started.")
        # E.g., self.db_connection = connect_to_db()

    def on_pause(self) -> None:
        """Called to pause background tasks temporarily."""
        print(f"[{self.name}] Paused.")

    def on_destroy(self) -> None:
        """Called during graceful shutdown."""
        print(f"[{self.name}] Destroyed. Cleaning up resources...")
        # E.g., if self.db_connection: self.db_connection.close()

    def execute(self, action: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """
        Main entry point for plugin execution.
        """
        if action == "hello":
            return f"Hello, {payload.get('name', 'World')}!"
        elif action == "complex_task":
            return self._do_complex_task(payload)
        else:
            raise ValueError(f"Unknown action: {action}")

    def _do_complex_task(self, payload: Dict[str, Any]) -> str:
        return "Complex task completed successfully."
