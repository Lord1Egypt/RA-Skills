"""CLI Commands for LLM Engine management."""

import argparse
import sys
from typing import Optional

from kb.base.command import BaseCommand
from kb.base.config import KBConfig
from kb.commands import register_command
from kb.biblio.engine.factory import create_engine
from kb.biblio.config import LLMConfig


@register_command
class EngineListCommand(BaseCommand):
    """List available LLM engines."""

    name = "engine-list"
    help = "List available LLM engines"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add command arguments."""
        parser.add_argument("--verbose", "-v", action="store_true",
                          help="Show verbose engine details")

    def _execute(self) -> int:
        """Execute the command."""
        config = KBConfig.get_instance()
        llm_config = LLMConfig.get_instance()

        print("Available LLM Engines:")
        print("-" * 50)

        engines = [
            ("ollama", "Ollama API", llm_config.ollama_url),
            ("huggingface", "Hugging Face Transformers", llm_config.hf_model_name),
        ]

        for name, description, endpoint in engines:
            available = False
            try:
                engine = create_engine(llm_config) if llm_config.model_source == name else None
                if engine:
                    available = engine.is_available()
            except Exception as e:
                logger.warning(f"Engine check failed: {e}")
                availability = False
            status = "✅ Available" if available else "❌ Not available"

            print(f"\n{name}")
            print(f"  Description: {description}")
            print(f"  Status: {status}")
            print(f"  Endpoint: {endpoint}")

        return 0


@register_command
class EngineInfoCommand(BaseCommand):
    """Show detailed info about an engine."""

    name = "engine-info"
    help = "Show detailed information about an engine"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add command arguments."""
        parser.add_argument(
            "engine_name",
            choices=["ollama", "huggingface", "transformers"],
            help="Name of the engine to inspect"
        )

    def _execute(self) -> int:
        """Execute the command."""
        engine_name = self._args.engine_name

        if engine_name == "transformers":
            engine_name = "huggingface"

        llm_config = LLMConfig.get_instance()

        print(f"Engine: {engine_name}")
        print("-" * 50)

        if engine_name == "ollama":
            print(f"Type: Ollama API")
            print(f"URL: {llm_config.ollama_url}")
            print(f"Model: {llm_config.ollama_model}")
            print(f"Temperature: {llm_config.ollama_temperature}")
            print(f"Max Tokens: {llm_config.ollama_max_tokens}")

        elif engine_name == "huggingface":
            print(f"Type: Hugging Face Transformers")
            print(f"Model: {llm_config.hf_model_name}")
            print(f"Device: {llm_config.hf_device}")
            print(f"Quantization: {llm_config.hf_quantization or 'None'}")
            print(f"Temperature: {llm_config.hf_temperature}")
            print(f"Max Tokens: {llm_config.hf_max_tokens}")

        # Check availability via create_engine
        available = False
        try:
            if llm_config.model_source == engine_name:
                engine = create_engine(llm_config)
                available = engine.is_available()
            else:
                # Different engine than configured – try creating a config for it
                alt_config = LLMConfig(model_source=engine_name, skip_validation=True)
                engine = create_engine(alt_config)
                available = engine.is_available()
        except Exception as e:
            logger.warning(f"Engine check failed: {e}")
            availability = False
        print(f"\nAvailable: {'Yes' if available else 'No'}")

        if not available:
            print("\nTo enable this engine:")
            if engine_name == "ollama":
                print("  1. Install Ollama: https://ollama.com")
                print("  2. Start Ollama server")
                print("  3. Pull a model: ollama pull llama3.2")
            else:
                print("  1. Install dependencies:")
                print("     pip install torch transformers")
                print("  2. For quantization:")
                print("     pip install bitsandbytes")

        return 0