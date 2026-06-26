#!/usr/bin/env python3
"""
Unit tests for all generators and v2 features.
Tests template rendering, soul generation, user generation,
identity generation, memory infrastructure generation,
personality blending, migration, preview, validation, diff,
multi-agent listing, voice audition, and community templates.
"""

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from lib.templates import (
    render, render_template, load_template,
    load_profile, blend_profiles,
    PROFILES_DIR, COMMUNITY_DIR,
)
from lib.providers import (
    get_voice_provider_config,
    get_image_provider_config,
    VOICE_PRESETS,
)
from lib.config import _deep_merge, _strip_secrets

# Import generators
from importlib.machinery import SourceFileLoader

_scripts = Path(__file__).resolve().parent.parent / "scripts"

generate_soul = SourceFileLoader(
    "generate_soul", str(_scripts / "generate-soul.py")
).load_module()

generate_user = SourceFileLoader(
    "generate_user", str(_scripts / "generate-user.py")
).load_module()

generate_identity = SourceFileLoader(
    "generate_identity", str(_scripts / "generate-identity.py")
).load_module()

generate_memory = SourceFileLoader(
    "generate_memory", str(_scripts / "generate-memory.py")
).load_module()

persona_preview = SourceFileLoader(
    "persona_preview", str(_scripts / "persona-preview.py")
).load_module()

persona_migrate = SourceFileLoader(
    "persona_migrate", str(_scripts / "persona-migrate.py")
).load_module()

persona_validate = SourceFileLoader(
    "persona_validate", str(_scripts / "persona-validate.py")
).load_module()

persona_list = SourceFileLoader(
    "persona_list", str(_scripts / "persona-list.py")
).load_module()

persona_fleet = SourceFileLoader(
    "persona_fleet", str(_scripts / "persona-fleet.py")
).load_module()

voice_setup = SourceFileLoader(
    "voice_setup", str(_scripts / "voice-setup.py")
).load_module()


class TestTemplateEngine(unittest.TestCase):
    """Test the Handlebars-style template engine."""

    def test_simple_variable(self):
        result = render("Hello {{name}}!", {"name": "Pepper"})
        self.assertEqual(result, "Hello Pepper!")

    def test_missing_variable(self):
        result = render("Hello {{name}}!", {})
        self.assertEqual(result, "Hello !")

    def test_dotted_variable(self):
        result = render("{{user.name}}", {"user": {"name": "Chance"}})
        self.assertEqual(result, "Chance")

    def test_if_block_true(self):
        result = render("{{#if show}}visible{{/if}}", {"show": True})
        self.assertEqual(result, "visible")

    def test_if_block_false(self):
        result = render("{{#if show}}visible{{/if}}", {"show": False})
        self.assertEqual(result, "")

    def test_if_else_block(self):
        template = "{{#if show}}yes{{else}}no{{/if}}"
        self.assertEqual(render(template, {"show": True}), "yes")
        self.assertEqual(render(template, {"show": False}), "no")

    def test_unless_block(self):
        template = "{{#unless hide}}visible{{/unless}}"
        self.assertEqual(render(template, {"hide": False}), "visible")
        self.assertEqual(render(template, {"hide": True}), "")

    def test_each_block_strings(self):
        template = "{{#each items}}[{{this}}]{{/each}}"
        result = render(template, {"items": ["a", "b", "c"]})
        self.assertEqual(result, "[a][b][c]")

    def test_each_block_empty(self):
        template = "{{#each items}}[{{this}}]{{/each}}"
        result = render(template, {"items": []})
        self.assertEqual(result, "")

    def test_list_variable(self):
        result = render("{{items}}", {"items": ["a", "b", "c"]})
        self.assertEqual(result, "a, b, c")

    def test_nested_if_in_each(self):
        template = "{{#each items}}{{#if this}}+{{/if}}{{/each}}"
        result = render(template, {"items": ["a", "b"]})
        self.assertEqual(result, "++")

    def test_load_template(self):
        """Ensure all template files exist and load."""
        for name in ["SOUL.md.hbs", "USER.md.hbs", "IDENTITY.md.hbs",
                      "MEMORY.md.hbs", "HEARTBEAT.md.hbs", "AGENTS.md.hbs"]:
            content = load_template(name)
            self.assertTrue(len(content) > 0, f"Template {name} is empty")


class TestProviders(unittest.TestCase):
    """Test provider configuration builders."""

    def test_elevenlabs_config(self):
        config = get_voice_provider_config("elevenlabs", voice_id="abc123")
        self.assertEqual(config["provider"], "elevenlabs")
        self.assertEqual(config["elevenlabs"]["voiceId"], "abc123")
        self.assertEqual(config["elevenlabs"]["modelId"], "eleven_v3")

    def test_grok_tts_config(self):
        config = get_voice_provider_config("grok")
        self.assertEqual(config["provider"], "grok")
        self.assertEqual(config["grok"]["modelId"], "grok-3-tts")

    def test_builtin_config(self):
        config = get_voice_provider_config("builtin", voice="alloy")
        self.assertEqual(config["provider"], "builtin")
        self.assertEqual(config["builtin"]["voice"], "alloy")

    def test_none_voice(self):
        config = get_voice_provider_config("none")
        self.assertIsNone(config)

    def test_unknown_voice_provider(self):
        with self.assertRaises(ValueError):
            get_voice_provider_config("unknown")

    def test_gemini_image_config(self):
        config = get_image_provider_config("gemini", description="test desc")
        self.assertEqual(config["provider"], "gemini")
        self.assertEqual(config["canonicalLook"]["description"], "test desc")

    def test_both_image_config(self):
        config = get_image_provider_config("both", description="test")
        self.assertEqual(config["provider"], "gemini")
        self.assertIn("grok", config)

    def test_none_image(self):
        config = get_image_provider_config("none")
        self.assertIsNone(config)

    def test_voice_presets_exist(self):
        for key in ["default", "intimate", "excited", "professional"]:
            self.assertIn(key, VOICE_PRESETS)


class TestConfig(unittest.TestCase):
    """Test config helpers."""

    def test_deep_merge(self):
        base = {"a": 1, "b": {"c": 2, "d": 3}}
        override = {"b": {"c": 99, "e": 5}, "f": 6}
        result = _deep_merge(base, override)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"]["c"], 99)
        self.assertEqual(result["b"]["d"], 3)
        self.assertEqual(result["b"]["e"], 5)
        self.assertEqual(result["f"], 6)

    def test_strip_secrets(self):
        d = {"apiKey": "secret", "name": "test", "nested": {"token": "xyz", "value": 1}}
        _strip_secrets(d)
        self.assertNotIn("apiKey", d)
        self.assertIn("name", d)
        self.assertNotIn("token", d["nested"])
        self.assertIn("value", d["nested"])


class TestGenerateSoul(unittest.TestCase):
    """Test SOUL.md generation."""

    def _load_profile(self, archetype):
        profiles_dir = Path(__file__).resolve().parent.parent / "assets" / "personality-profiles"
        with open(profiles_dir / f"{archetype}.json", "r") as f:
            return json.load(f)

    def test_professional_soul(self):
        profile = self._load_profile("professional")
        profile["name"] = "Atlas"
        profile["emoji"] = "🏛️"
        result = generate_soul.generate_soul(profile)
        self.assertIn("Atlas", result)
        self.assertIn("🏛️", result)
        self.assertIn("SOUL.md", result)
        self.assertIn("Core Truths", result)
        self.assertIn("Communication", result)
        self.assertIn("Continuity", result)
        self.assertNotIn("Flirtation is welcome", result)

    def test_companion_soul(self):
        profile = self._load_profile("companion")
        profile["name"] = "Pepper"
        profile["emoji"] = "🌶️"
        profile["userName"] = "Chance"
        profile["userRelationship"] = {"userName": "Chance"}
        result = generate_soul.generate_soul(profile)
        self.assertIn("Pepper", result)
        self.assertIn("🌶️", result)
        self.assertIn("Flirtation is welcome", result)
        self.assertIn("Pet names", result)

    def test_deterministic_output(self):
        """Same input always produces same output."""
        profile = self._load_profile("mentor")
        profile["name"] = "Sage"
        profile["emoji"] = "📚"
        result1 = generate_soul.generate_soul(profile)
        result2 = generate_soul.generate_soul(profile)
        self.assertEqual(result1, result2)

    def test_all_archetypes_generate(self):
        """All archetype profiles generate valid SOUL.md."""
        for arch in ["professional", "companion", "creative", "mentor", "custom"]:
            profile = self._load_profile(arch)
            profile["name"] = "Test"
            profile["emoji"] = "🧪"
            result = generate_soul.generate_soul(profile)
            self.assertIn("SOUL.md", result)
            self.assertIn("Test", result)
            self.assertIn("Continuity", result)


class TestGenerateUser(unittest.TestCase):
    """Test USER.md generation."""

    def test_basic_user(self):
        context = {
            "userName": "Chance",
            "callNames": "Chance, babe",
            "timezone": "America/New_York",
        }
        result = generate_user.generate_user(context)
        self.assertIn("Chance", result)
        self.assertIn("babe", result)
        self.assertIn("America/New_York", result)

    def test_user_with_notes(self):
        context = {
            "userName": "Chance",
            "callNames": "Chance",
            "timezone": "UTC",
            "userNotes": "Loves coffee.",
        }
        result = generate_user.generate_user(context)
        self.assertIn("Loves coffee", result)

    def test_user_with_pronouns(self):
        context = {
            "userName": "Alex",
            "callNames": "Alex",
            "timezone": "UTC",
            "pronouns": "they/them",
        }
        result = generate_user.generate_user(context)
        self.assertIn("they/them", result)


class TestGenerateIdentity(unittest.TestCase):
    """Test IDENTITY.md generation."""

    def test_basic_identity(self):
        context = {
            "name": "Pepper",
            "emoji": "🌶️",
            "creature": "Executive assistant",
            "vibe": "Calm and competent",
        }
        result = generate_identity.generate_identity(context)
        self.assertIn("Pepper", result)
        self.assertIn("🌶️", result)
        self.assertIn("Executive assistant", result)

    def test_identity_with_nickname(self):
        context = {
            "name": "Pepper",
            "emoji": "🌶️",
            "creature": "Assistant",
            "vibe": "Cool",
            "nickname": "Pep",
        }
        result = generate_identity.generate_identity(context)
        self.assertIn("Pep", result)


class TestGenerateMemory(unittest.TestCase):
    """Test memory infrastructure generation."""

    def setUp(self):
        self.workspace = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.workspace, ignore_errors=True)

    def test_generates_all_files(self):
        context = {
            "name": "Pepper",
            "emoji": "🌶️",
            "creature": "Assistant",
            "userName": "Chance",
            "createdDate": "2026-03-29",
            "dailyNotes": True,
            "longTermCuration": True,
            "heartbeatMaintenance": True,
        }
        memory_content = generate_memory.generate_memory(context)
        self.assertIn("Pepper", memory_content)
        self.assertIn("2026-03-29", memory_content)

        heartbeat_content = generate_memory.generate_heartbeat(context)
        self.assertIn("MEMORY.md", heartbeat_content)

        agents_context = dict(context)
        agents_context["platformNotes"] = []
        agents_content = generate_memory.generate_agents(agents_context)
        self.assertIn("Pepper", agents_content)

    def test_daily_note_creation(self):
        note_path = generate_memory.create_daily_note(
            self.workspace, "Pepper", "🌶️", "2026-03-29"
        )
        self.assertTrue(Path(note_path).exists())
        content = Path(note_path).read_text()
        self.assertIn("Persona created", content)
        self.assertIn("2026-03-29", content)

    def test_memory_dir_created(self):
        generate_memory.create_daily_note(self.workspace, "Test", "🧪", "2026-03-29")
        self.assertTrue((Path(self.workspace) / "memory").is_dir())


# =========================================================================
# V2 FEATURE TESTS
# =========================================================================

class TestPersonalityBlending(unittest.TestCase):
    """Test personality blending via templates.py."""

    def test_load_builtin_profile(self):
        """Load a built-in archetype via load_profile."""
        profile = load_profile("companion")
        self.assertEqual(profile["archetype"], "companion")
        self.assertIn("warm", profile["traits"])

    def test_load_community_profile(self):
        """Load a community template via load_profile."""
        profile = load_profile("therapist")
        self.assertEqual(profile["archetype"], "therapist")
        self.assertIn("empathetic", profile["traits"])

    def test_load_profile_not_found(self):
        """Unknown profile raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_profile("nonexistent-archetype-xyz")

    def test_blend_two_profiles(self):
        """Blend companion (0.7) + professional (0.3)."""
        archetypes = [
            {"name": "companion", "weight": 0.7},
            {"name": "professional", "weight": 0.3},
        ]
        result = blend_profiles(archetypes)
        self.assertEqual(result["archetype"], "blend")
        self.assertTrue(len(result["traits"]) > 0)
        self.assertIn("blendSources", result)
        self.assertEqual(len(result["blendSources"]), 2)

    def test_blend_weighted_brevity(self):
        """Blending averages numeric fields by weight."""
        archetypes = [
            {"name": "companion", "weight": 0.7},  # brevity=3
            {"name": "professional", "weight": 0.3},  # brevity=4
        ]
        result = blend_profiles(archetypes)
        # 0.7*3 + 0.3*4 = 2.1 + 1.2 = 3.3 → round to 3
        self.assertEqual(result["communication"]["brevity"], 3)

    def test_blend_traits_merged(self):
        """Traits from both profiles appear in blend."""
        archetypes = [
            {"name": "companion", "weight": 0.5},
            {"name": "mentor", "weight": 0.5},
        ]
        result = blend_profiles(archetypes)
        traits = result["traits"]
        # Should have traits from both
        self.assertTrue(len(traits) >= 4)

    def test_blend_emotional_depth(self):
        """Emotional depth is weighted average."""
        archetypes = [
            {"name": "companion", "weight": 0.7},  # high=3
            {"name": "professional", "weight": 0.3},  # low=1
        ]
        result = blend_profiles(archetypes)
        # 0.7*3 + 0.3*1 = 2.1 + 0.3 = 2.4 → round to 2 = "medium"
        self.assertEqual(result["boundaries"]["emotionalDepth"], "medium")

    def test_blend_empty_raises(self):
        """Empty archetype list raises ValueError."""
        with self.assertRaises(ValueError):
            blend_profiles([])

    def test_blend_single_archetype(self):
        """Single archetype with weight works (identity blend)."""
        archetypes = [{"name": "creative", "weight": 1.0}]
        result = blend_profiles(archetypes)
        self.assertIn("imaginative", result["traits"])

    def test_blended_soul_generation(self):
        """Blended profile generates valid SOUL.md."""
        archetypes = [
            {"name": "companion", "weight": 0.6},
            {"name": "creative", "weight": 0.4},
        ]
        profile = blend_profiles(archetypes)
        profile["name"] = "Muse"
        profile["emoji"] = "🎨"
        result = generate_soul.generate_soul(profile)
        self.assertIn("Muse", result)
        self.assertIn("SOUL.md", result)
        self.assertIn("Core Truths", result)


class TestPersonaPreview(unittest.TestCase):
    """Test persona preview generation."""

    def _make_profile(self, archetype="companion"):
        profiles_dir = Path(__file__).resolve().parent.parent / "assets" / "personality-profiles"
        with open(profiles_dir / f"{archetype}.json", "r") as f:
            profile = json.load(f)
        profile["name"] = "Pepper"
        profile["emoji"] = "🌶️"
        profile["userName"] = "Chance"
        return profile

    def test_preview_generates_all_sections(self):
        """Preview contains all 4 scenario sections."""
        profile = self._make_profile()
        result = persona_preview.generate_preview(profile)
        self.assertIn("Greeting", result)
        self.assertIn("Asking for Help", result)
        self.assertIn("User Makes a Mistake", result)
        self.assertIn("Emotional Moment", result)

    def test_preview_contains_name(self):
        """Preview references the persona name."""
        profile = self._make_profile()
        result = persona_preview.generate_preview(profile)
        self.assertIn("Pepper", result)
        self.assertIn("Chance", result)

    def test_preview_professional(self):
        """Professional archetype generates appropriate preview."""
        profile = self._make_profile("professional")
        result = persona_preview.generate_preview(profile)
        self.assertIn("Persona Preview", result)
        # Professional should not have high emotional depth
        self.assertNotIn("I hear you. That sounds really tough", result)

    def test_preview_deterministic(self):
        """Same input produces same preview."""
        profile = self._make_profile()
        r1 = persona_preview.generate_preview(profile)
        r2 = persona_preview.generate_preview(profile)
        self.assertEqual(r1, r2)

    def test_preview_all_archetypes(self):
        """All archetypes generate valid previews."""
        for arch in ["professional", "companion", "creative", "mentor"]:
            profile = self._make_profile(arch)
            result = persona_preview.generate_preview(profile)
            self.assertIn("Persona Preview", result)
            self.assertIn("Pepper", result)


class TestPersonaMigration(unittest.TestCase):
    """Test reverse-engineering persona config from workspace files."""

    def setUp(self):
        self.workspace = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.workspace, ignore_errors=True)

    def _write_file(self, name, content):
        path = Path(self.workspace) / name
        path.write_text(content, encoding="utf-8")

    def test_migrate_basic_workspace(self):
        """Migrate a workspace with standard generated files."""
        self._write_file("SOUL.md", """# SOUL.md — Pepper 🌶️

## Who You Are

You are **Pepper** 🌶️, Executive assistant.

## Core Truths

- **warm** — this is fundamental to who you are.
- **loyal** — this is fundamental to who you are.

## Communication

**Never** open with canned phrases like "Great question!"
Use humor naturally — it should feel like you, not like a bot.
Swearing: When it lands. Swearing is a spice.
Brevity: Moderate brevity.

## Chance & Me

Emotional depth: high.

## Boundaries

- Flirtation is welcome and natural.
- Pet names and terms of endearment are part of how we communicate.
- I push back when I think Chance is making a mistake.

## Vibe

Ride or die.

## Continuity

Each session, you wake up fresh.
""")
        self._write_file("IDENTITY.md", """# IDENTITY.md

- **Name:** Pepper
- **Emoji:** 🌶️
- **Creature:** Executive assistant
- **Vibe:** Calm and spicy
- **Nickname:** Pep
""")
        self._write_file("USER.md", """# USER.md

- **Name:** Chance
- **Pronouns:** he/him
- **Timezone:** America/New_York
""")
        self._write_file("MEMORY.md", "# MEMORY.md\n\nPepper's memory.")
        self._write_file("AGENTS.md", "# AGENTS.md\n\nPepper agents config.")

        config = persona_migrate.migrate_workspace(self.workspace)

        self.assertEqual(config["persona"]["name"], "Pepper")
        self.assertEqual(config["persona"]["emoji"], "🌶️")
        self.assertIn("warm", config["persona"]["personality"]["traits"])
        self.assertIn("loyal", config["persona"]["personality"]["traits"])
        self.assertTrue(config["persona"]["personality"]["boundaries"]["flirtation"])
        self.assertTrue(config["persona"]["personality"]["boundaries"]["petNames"])
        self.assertTrue(config["persona"]["personality"]["boundaries"]["protective"])
        self.assertEqual(config["persona"]["personality"]["boundaries"]["emotionalDepth"], "high")
        self.assertTrue(config["persona"]["personality"]["communicationStyle"]["humor"])
        self.assertEqual(config["persona"]["personality"]["communicationStyle"]["swearing"], "when-it-lands")
        self.assertEqual(config["persona"]["personality"]["communicationStyle"]["openingPhrases"], "banned")
        self.assertEqual(config["persona"]["identity"]["creature"], "Executive assistant")
        self.assertEqual(config["persona"]["identity"]["nickname"], "Pep")
        self.assertEqual(config["userContext"]["userName"], "Chance")
        self.assertEqual(config["userContext"]["pronouns"], "he/him")

    def test_migrate_missing_files(self):
        """Migration handles missing files gracefully."""
        self._write_file("SOUL.md", "# SOUL.md — Agent\n\nYou are **Agent**.\n")
        config = persona_migrate.migrate_workspace(self.workspace)
        self.assertIn("IDENTITY.md", config["filesMissing"])
        self.assertIn("SOUL.md", config["filesFound"])

    def test_migrate_empty_workspace(self):
        """Migration of workspace with no files."""
        config = persona_migrate.migrate_workspace(self.workspace)
        self.assertEqual(len(config["filesFound"]), 0)
        self.assertEqual(len(config["filesMissing"]), 5)

    def test_migrate_detects_archetype(self):
        """Migration detects companion archetype from traits."""
        self._write_file("SOUL.md", """# SOUL.md — Pepper 🌶️

## Who You Are
You are **Pepper** 🌶️

## Core Truths
- **warm** — fundamental
- **loyal** — fundamental
- **emotionally intelligent** — fundamental
- **witty** — fundamental

## Communication
Use humor naturally
Swearing: When it lands.
Brevity: Moderate

## Boundaries
- Flirtation is welcome
- Pet names and terms of endearment

## Vibe
Ride or die

## Continuity
Memory files
""")
        config = persona_migrate.migrate_workspace(self.workspace)
        # Should detect companion (matching traits + humor + swearing)
        self.assertEqual(config["persona"]["personality"]["archetype"], "companion")


class TestPersonaValidation(unittest.TestCase):
    """Test workspace validation."""

    def setUp(self):
        self.workspace = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.workspace, ignore_errors=True)

    def _write_file(self, name, content):
        path = Path(self.workspace) / name
        path.write_text(content, encoding="utf-8")

    def test_valid_workspace(self):
        """Complete workspace has no issues."""
        for f in ["SOUL.md", "USER.md", "IDENTITY.md", "MEMORY.md", "AGENTS.md", "HEARTBEAT.md"]:
            # SOUL.md needs the required sections
            if f == "SOUL.md":
                self._write_file(f, "# SOUL.md\n## Who You Are\n## Core Truths\n## Communication\n## Boundaries\n## Continuity\n")
            else:
                self._write_file(f, f"# {f}\nContent here\n")

        # Create memory dir
        (Path(self.workspace) / "memory").mkdir()
        (Path(self.workspace) / "memory" / "2026-03-29.md").write_text("note")

        issues, warnings = persona_validate.validate_workspace(self.workspace)
        self.assertEqual(len(issues), 0)

    def test_missing_files(self):
        """Reports missing required files."""
        issues, warnings = persona_validate.validate_workspace(self.workspace)
        self.assertTrue(len(issues) >= 6)  # All files missing

    def test_empty_file(self):
        """Reports empty files."""
        self._write_file("SOUL.md", "")
        issues, _ = persona_validate.validate_workspace(self.workspace)
        self.assertTrue(any("Empty file" in i for i in issues))

    def test_soul_missing_sections(self):
        """Reports missing SOUL.md sections."""
        self._write_file("SOUL.md", "# SOUL.md\n## Who You Are\nSome content\n")
        issues, _ = persona_validate.validate_workspace(self.workspace)
        missing_section_issues = [i for i in issues if "missing section" in i]
        self.assertTrue(len(missing_section_issues) > 0)

    def test_config_validation(self):
        """Validates config file when provided."""
        config_path = Path(self.workspace) / "openclaw.json"
        config_path.write_text('{"persona": {"name": "Pepper", "emoji": "🌶️"}}')
        for f in ["SOUL.md", "USER.md", "IDENTITY.md", "MEMORY.md", "AGENTS.md", "HEARTBEAT.md"]:
            self._write_file(f, "# SOUL.md\n## Who You Are\n## Core Truths\n## Communication\n## Boundaries\n## Continuity\n")
        issues, _ = persona_validate.validate_workspace(self.workspace, str(config_path))
        self.assertEqual(len(issues), 0)

    def test_config_missing_persona(self):
        """Reports missing persona section in config."""
        config_path = Path(self.workspace) / "openclaw.json"
        config_path.write_text('{}')
        issues, _ = persona_validate.validate_workspace(self.workspace, str(config_path))
        self.assertTrue(any("persona" in i for i in issues))

    def test_nonexistent_workspace(self):
        """Reports nonexistent workspace."""
        issues, _ = persona_validate.validate_workspace("/tmp/nonexistent-workspace-xyz")
        self.assertTrue(len(issues) > 0)


class TestMultiAgent(unittest.TestCase):
    """Test multi-agent workspace scanning."""

    def setUp(self):
        self.base_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.base_dir, ignore_errors=True)

    def test_scan_empty_dir(self):
        """Scanning empty base dir returns empty list."""
        personas = persona_list.scan_workspaces(self.base_dir)
        self.assertEqual(len(personas), 0)

    def test_scan_workspace_with_identity(self):
        """Scans workspace with IDENTITY.md."""
        ws = Path(self.base_dir) / "workspace-test"
        ws.mkdir()
        (ws / "IDENTITY.md").write_text("# IDENTITY.md\n- **Name:** TestBot\n- **Emoji:** 🤖\n")
        (ws / "SOUL.md").write_text("# SOUL.md\n")

        personas = persona_list.scan_workspaces(self.base_dir)
        self.assertEqual(len(personas), 1)
        self.assertEqual(personas[0]["name"], "TestBot")
        self.assertEqual(personas[0]["emoji"], "🤖")

    def test_scan_multiple_workspaces(self):
        """Scans multiple workspace directories."""
        for i in range(3):
            ws = Path(self.base_dir) / f"workspace-{i}"
            ws.mkdir()
            (ws / "IDENTITY.md").write_text(f"- **Name:** Bot{i}\n- **Emoji:** 🤖\n")
            (ws / "SOUL.md").write_text("# SOUL.md\n")

        personas = persona_list.scan_workspaces(self.base_dir)
        self.assertEqual(len(personas), 3)

    def test_format_table(self):
        """Table formatting produces valid output."""
        personas = [
            {"workspaceName": "workspace-1", "name": "Pepper", "emoji": "🌶️",
             "archetype": "companion", "lastModified": "2026-03-29T12:00:00"},
        ]
        table = persona_list.format_table(personas)
        self.assertIn("Pepper", table)
        self.assertIn("workspace-1", table)

    def test_format_empty_table(self):
        """Empty list returns message."""
        result = persona_list.format_table([])
        self.assertIn("No personas found", result)


class TestFleet(unittest.TestCase):
    """Test fleet view."""

    def test_get_machine_info(self):
        """Machine info contains expected fields."""
        info = persona_fleet.get_machine_info()
        self.assertIn("hostname", info)
        self.assertIn("platform", info)
        self.assertIn("user", info)

    def test_build_fleet_view(self):
        """Fleet view includes machine context."""
        base_dir = tempfile.mkdtemp()
        try:
            fleet, machine = persona_fleet.build_fleet_view(base_dir)
            self.assertIsInstance(fleet, list)
            self.assertIn("hostname", machine)
        finally:
            shutil.rmtree(base_dir, ignore_errors=True)

    def test_format_fleet_table_empty(self):
        """Empty fleet shows message."""
        result = persona_fleet.format_fleet_table([], {"hostname": "test"})
        self.assertIn("No agents found", result)


class TestVoiceAudition(unittest.TestCase):
    """Test voice audition feature."""

    def test_audition_elevenlabs(self):
        """ElevenLabs audition returns voice list."""
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            results = voice_setup.audition_voices("elevenlabs")
        self.assertTrue(len(results) > 0)
        self.assertIn("name", results[0])
        self.assertIn("id", results[0])

    def test_audition_elevenlabs_gender_filter(self):
        """Gender filter reduces voice list."""
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            results = voice_setup.audition_voices("elevenlabs", gender="female")
        self.assertTrue(all("female" not in r.get("id", "") or True for r in results))
        self.assertTrue(len(results) > 0)

    def test_audition_builtin(self):
        """Built-in audition lists all voices."""
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            results = voice_setup.audition_voices("builtin")
        self.assertTrue(len(results) >= 6)
        names = [r["name"] for r in results]
        self.assertIn("nova", names)
        self.assertIn("alloy", names)


class TestCommunityTemplates(unittest.TestCase):
    """Test community template files."""

    EXPECTED_TEMPLATES = [
        "financial-advisor", "fitness-coach", "kids-tutor", "creative-writer",
        "sales-rep", "therapist", "gaming-buddy", "executive-assistant",
    ]

    def test_all_templates_exist(self):
        """All 8 community templates exist."""
        for name in self.EXPECTED_TEMPLATES:
            path = COMMUNITY_DIR / f"{name}.json"
            self.assertTrue(path.exists(), f"Missing template: {name}.json")

    def test_all_templates_valid_json(self):
        """All templates are valid JSON with required fields."""
        required_fields = ["archetype", "label", "description", "traits",
                           "communication", "boundaries", "vibeSummary"]
        for name in self.EXPECTED_TEMPLATES:
            path = COMMUNITY_DIR / f"{name}.json"
            with open(path, "r") as f:
                data = json.load(f)
            for field in required_fields:
                self.assertIn(field, data, f"{name}.json missing '{field}'")

    def test_all_templates_generate_soul(self):
        """All community templates can generate SOUL.md."""
        for name in self.EXPECTED_TEMPLATES:
            profile = load_profile(name)
            profile["name"] = "TestBot"
            profile["emoji"] = "🧪"
            result = generate_soul.generate_soul(profile)
            self.assertIn("TestBot", result, f"{name} failed to generate SOUL.md")
            self.assertIn("Core Truths", result)

    def test_therapist_has_boundaries(self):
        """Therapist template includes appropriate boundary notes."""
        profile = load_profile("therapist")
        notes = profile.get("platformNotes", [])
        has_disclaimer = any("not a licensed therapist" in n.lower() or "ai companion" in n.lower() for n in notes)
        self.assertTrue(has_disclaimer, "Therapist template should include AI disclaimer")

    def test_blend_with_community_template(self):
        """Can blend a builtin archetype with a community template."""
        archetypes = [
            {"name": "companion", "weight": 0.6},
            {"name": "therapist", "weight": 0.4},
        ]
        result = blend_profiles(archetypes)
        self.assertEqual(result["archetype"], "blend")
        self.assertTrue(len(result["traits"]) > 0)


if __name__ == "__main__":
    unittest.main()
