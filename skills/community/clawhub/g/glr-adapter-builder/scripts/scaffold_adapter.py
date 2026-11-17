#!/usr/bin/env python3
"""Create a safe, synthetic-first GLR adapter development lane."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SKILL_ROOT = Path(__file__).resolve().parents[1]
_ASSETS = _SKILL_ROOT / "assets"
_PACKAGE = re.compile(r"^[a-z][a-z0-9_]*$")
_ENVIRONMENT_ID = re.compile(r"^[a-z][a-z0-9_.-]*$")
_UPSTREAM_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
# The generated adapter imports the current public Python contract surface.
# Keep one compatible-release series here and verify it against a real clean
# install in tests; do not copy the standalone CLI version into each template.
PYTHON_API_VERSION = "0.26.0"  # x-release-please-version
PYTHON_API_COMPATIBLE_RELEASE = ".".join(PYTHON_API_VERSION.split(".")[:2])


def _load_asset(name: str) -> dict[str, Any]:
    with (_ASSETS / name).open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise TypeError(f"asset {name} must contain a JSON object")
    return value


def _load_text_asset(name: str, **replacements: str) -> str:
    content = (_ASSETS / name).read_text(encoding="utf-8")
    for key, value in replacements.items():
        content = content.replace(f"@@{key.upper()}@@", value)
    unresolved = re.findall(r"@@[A-Z_]+@@", content)
    if unresolved:
        raise ValueError(f"asset {name} has unresolved replacements: {unresolved}")
    return content


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _environment_module(start_mode: str) -> str:
    if start_mode == "reset":
        return '''"""Synthetic seam; replace its semantics with the authorized adapter."""

from game_learning_runtime.contracts import TensorTree, TimeStep
from game_learning_runtime.environment import GameEnvironment
from game_learning_runtime.examples import CounterEnvironment, always_increment


def create_environment() -> GameEnvironment:
    """Return a trainable synthetic environment for the initial green baseline."""

    return CounterEnvironment(target=3, max_steps=5)


def synthetic_policy(timestep: TimeStep) -> TensorTree:
    return always_increment(timestep)


__all__ = ["create_environment", "synthetic_policy"]
'''

    return '''"""Synthetic live-attach seam; it makes no physical reset claim."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from game_learning_runtime.contracts import TensorTree, TimeStep
from game_learning_runtime.environment import GameEnvironment
from game_learning_runtime.errors import ContractViolation
from game_learning_runtime.examples import CounterEnvironment, always_increment
from game_learning_runtime.specs import EnvironmentSpec


class SyntheticAttachEnvironment(CounterEnvironment):
    """Runnable attach baseline to replace with an authorized live adapter."""

    def __init__(self) -> None:
        super().__init__(target=3, max_steps=5)
        source = self._spec
        self._spec = EnvironmentSpec(
            environment_id=source.environment_id,
            observation=source.observation,
            action=source.action,
            reward=source.reward,
            done=source.done,
            action_mask=source.action_mask,
            protocol_version=source.protocol_version,
            capabilities=source.capabilities | {"live-attach"},
            metadata=source.metadata,
        )

    def reset(
        self, *, seed: int | None = None, options: Mapping[str, Any] | None = None
    ) -> TimeStep:
        del seed, options
        raise ContractViolation("physical reset is unavailable in attach mode")

    def attach(self, *, options: Mapping[str, Any] | None = None) -> TimeStep:
        return super().reset(options=options)


def create_environment() -> GameEnvironment:
    """Return a trainable synthetic live-attach baseline."""

    return SyntheticAttachEnvironment()


def synthetic_policy(timestep: TimeStep) -> TensorTree:
    return always_increment(timestep)


__all__ = ["SyntheticAttachEnvironment", "create_environment", "synthetic_policy"]
'''


def _test_module(package: str) -> str:
    return f"""from game_learning_runtime import (
    EpisodeRewardGuard,
    RewardComposer,
    RewardSignal,
    load_reward_safety_config,
    load_training_config,
)
from game_learning_runtime.project import find_project
from game_learning_runtime.testing import run_environment_conformance

from {package}.environment import create_environment, synthetic_policy

ROOT = find_project(__file__).parent


def test_synthetic_contract_is_trainable() -> None:
    config = load_training_config(ROOT / "training.json")
    report = run_environment_conformance(
        create_environment(),
        synthetic_policy,
        steps=3,
        start_mode=config.lifecycle.start_mode,
    )
    assert report.transition_count == 3


def test_reward_configuration_is_executable_data_not_an_expression() -> None:
    config = load_training_config(ROOT / "training.json")
    result = RewardComposer(config).compose(
        [RewardSignal(name="progress", source="runtime", value=0.25)]
    )
    assert result.total == 0.25


def test_failed_episode_cannot_become_positive_from_dense_shaping() -> None:
    config = load_training_config(ROOT / "training.json")
    guard = EpisodeRewardGuard(
        config,
        load_reward_safety_config(ROOT / "reward-safety.json"),
    )
    for _ in range(10):
        guard.compose([RewardSignal(name="progress", source="runtime", value=1)])
    terminal = guard.compose(
        [
            RewardSignal(name="progress", source="runtime", value=1),
            RewardSignal(name="outcome", source="runtime", value=-1),
        ],
        terminal=True,
    )
    assert terminal.episode_total <= 0
"""


def _pyproject(package: str) -> str:
    project = package.replace("_", "-")
    runtime_dependency = f"game-learning-runtime~={PYTHON_API_COMPATIBLE_RELEASE}.0"
    return f'''[build-system]
requires = ["editables>=0.5", "hatchling>=1.27"]
build-backend = "hatchling.build"

[project]
name = "{project}"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
  "{runtime_dependency}",
]

[dependency-groups]
dev = ["build>=1.2", "editables>=0.5", "hatchling>=1.27", "mypy>=1.15", "pytest>=8.3", "ruff>=0.11"]

[tool.hatch.build.targets.wheel]
packages = ["src/{package}"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["--import-mode=importlib", "--strict-config", "--strict-markers"]

[tool.ruff.lint]
select = ["E", "F", "I", "TID251"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint.flake8-tidy-imports.banned-api]
"sys.path" = {{ msg = "Install the owning package; never mutate import search paths." }}
'''


def _vx_toml(package: str) -> str:
    return f'''[project]
name = "{package.replace("_", "-")}"

[tools]
python = "3.12.13"
uv = "0.12.7"
just = "1.58.0"

[env]
UV_PROJECT_ENVIRONMENT = ".venv-glr"

[scripts]
setup = "vx just setup"
check = "vx just check"
ci = "vx just ci"
package-check = "vx just package-check"
test = "vx just test"
train = "vx just train"
reproduce = "vx just reproduce"
package-runtime = "vx just package-runtime"
'''


def _justfile() -> str:
    windows_shell = (
        'set windows-shell := ["powershell.exe", "-NoLogo", "-NoProfile", '
        '"-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command"]'
    )
    return f"""set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
{windows_shell}
export UV_PROJECT_ENVIRONMENT := ".venv-glr"

default: check

setup:
    vx uv sync --python 3.12.13 --all-groups --no-install-project
    vx uv sync --python 3.12.13 --all-groups --no-build-isolation

lock-check:
    vx uv lock --check

lint:
    vx uv run python -m ruff check src tests scripts

typecheck:
    vx uv run python -m mypy src

test:
    vx uv run python -m pytest

check: setup lock-check lint typecheck test

package-check: setup
    vx uv run python scripts/check_wheel.py

ci: check package-check

train: setup
    vx uv run python scripts/train_reference.py --output .glr/exports/model-bundles/reference-model

reproduce:
    vx uv run python scripts/verify_bundle.py .glr/exports/model-bundles/reference-model

package-runtime output=".glr/exports/loader-packages/loader-package":
    vx uv run python scripts/package_runtime.py --output {{output}}
"""


def _runtime_integration(
    engine: str, access: str, *, loader: str | None = None
) -> dict[str, object]:
    if access == "source":
        return {
            "schema_version": "glr.runtime-integration.v2",
            "engine_family": engine,
            "integration_mode": "engine-plugin",
            "loader_family": None,
            "start_mode": "reset",
            "clock_mode": "manual-step",
            "observation_mode": "engine-state",
            "action_mode": "native",
            "transport_mode": "local-ipc",
            "seedable": True,
        }
    if access == "loader":
        return {
            "schema_version": "glr.runtime-integration.v2",
            "engine_family": engine,
            "integration_mode": "loader-plugin",
            "loader_family": loader,
            "start_mode": "attach",
            "clock_mode": "realtime",
            "observation_mode": "engine-state",
            "action_mode": "bounded-command",
            "transport_mode": "local-ipc",
            "seedable": False,
        }
    return {
        "schema_version": "glr.runtime-integration.v2",
        "engine_family": engine,
        "integration_mode": "external-attach",
        "loader_family": None,
        "start_mode": "attach",
        "clock_mode": "realtime",
        "observation_mode": "rendered",
        "action_mode": "bounded-input",
        "transport_mode": "local-ipc",
        "seedable": False,
    }


def _required_capabilities(access: str) -> list[str]:
    if access == "source":
        return sorted(
            {
                "authenticated",
                "deterministic-reset",
                "main-thread-dispatch",
                "manual-step",
                "native-action",
                "postcondition-verified",
                "reset",
                "semantic-observation",
                "step",
                "target-bound",
            }
        )
    if access == "loader":
        return sorted(
            {
                "authenticated",
                "bounded-command",
                "live-attach",
                "loader-plugin",
                "main-thread-dispatch",
                "postcondition-verified",
                "realtime",
                "semantic-observation",
                "step",
                "target-bound",
            }
        )
    return sorted(
        {
            "authenticated",
            "bounded-input",
            "input-lease",
            "live-attach",
            "postcondition-verified",
            "realtime",
            "rendered-observation",
            "step",
            "target-bound",
        }
    )


def _readme(
    package: str,
    environment_id: str,
    start_mode: str,
    *,
    engine: str,
    access: str | None,
    loader: str | None,
) -> str:
    integration = (
        "generic"
        if access is None
        else " ".join(item for item in (engine, access, loader) if item is not None)
    )
    return f"""# {package}

GLR adapter development lane for `{environment_id}` using `{start_mode}` start
semantics and the `{integration}` integration profile.

The initial environment is deliberately synthetic and trainable. Replace it
with an authorized runtime adapter while preserving the tests. Do not publish
local endpoints, paths, process/window identifiers, credentials, observations,
actions, or proprietary game data.

Research public gameplay sources into `knowledge/research-manifest.json` as
compact paraphrased claims with provenance. Guide research remains advisory;
reward authority comes from verified runtime signals in `training.json`.

```powershell
vx setup
vx run check
glr --project . --json doctor
glr --project . --json train
glr --project . --json play --bundle .glr/exports/model-bundles/model-bundle
```

`glr-project.toml` is the one official lifecycle entry. Its strict
`glr.lifecycle.v1` section owns every configuration reference and the modes
that this generated lane actually supports. `doctor` prints the resolved
schema and SHA-256 for each input before any role runs.

The trainer runs a deterministic synthetic behavior-cloning smoke test and writes a
checksummed model bundle under `.glr/exports/model-bundles/`. It proves the training and
reproduction plumbing only; it is not live runtime acceptance.

Read `QUALITY.md` for packaging, logging, and offline regression requirements.
Use `vx run ci` to combine static/unit and clean-wheel gates. Before upgrading
GLR, follow `FRAMEWORK_MIGRATION.md` and record results in `MIGRATIONS.md`.
"""


def _agent_interface(environment_id: str, *, start_mode: str) -> dict[str, object]:
    mutating_operations = ["step", "close"]
    if start_mode == "reset":
        mutating_operations.insert(0, "reset")
    return {
        "schema_version": "glr.agent-interface.v1",
        "environment_id": environment_id,
        "operations": ["describe", start_mode, "step", "close"],
        "mutating_operations": mutating_operations,
        "required_mutation_fields": ["episode_id", "expected_step_id"],
        "unknown_operations": "deny",
        "metadata_policy": "allowlist",
        "action_vocabulary": [],
    }


def _agents_md(package: str, *, loader: str | None) -> str:
    loader_note = "No loader is selected for this lane."
    if loader is not None:
        loader_note = (
            f"This lane uses the authorized `{loader}` loader template. Do not auto-discover "
            "or modify a game installation; require an explicit operator-selected target."
        )
    return _load_text_asset(
        "templates/AGENTS.template.md", package=package, loader_note=loader_note
    )


def _loader_deployment(engine: str, loader: str, version: str) -> dict[str, object]:
    if loader == "bepinex":
        return {
            "schema_version": "glr.loader-deployment.v1",
            "engine_family": engine,
            "loader_family": loader,
            "runtime_variant": "unity-mono",
            "upstream_repository": "https://github.com/BepInEx/BepInEx",
            "upstream_version": version,
            "upstream_license": "LGPL-2.1",
            "install_mode": "manual-explicit-target",
            "artifacts": [
                {
                    "source": "runtime/bepinex/bin/Release/netstandard2.0/GlrBridge.dll",
                    "destination": "BepInEx/plugins/GlrBridge/GlrBridge.dll",
                }
            ],
        }
    return {
        "schema_version": "glr.loader-deployment.v1",
        "engine_family": engine,
        "loader_family": loader,
        "runtime_variant": "ue4ss-lua",
        "upstream_repository": "https://github.com/UE4SS-RE/RE-UE4SS",
        "upstream_version": version,
        "upstream_license": "MIT",
        "install_mode": "manual-explicit-target",
        "artifacts": [
            {
                "source": "runtime/ue4ss/GLRBridge/Scripts/main.lua",
                "destination": "Mods/GLRBridge/Scripts/main.lua",
            }
        ],
    }


def _bepinex_project() -> str:
    return """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>netstandard2.0</TargetFramework>
    <LangVersion>latest</LangVersion>
    <Nullable>enable</Nullable>
    <AssemblyName>GlrBridge</AssemblyName>
    <RootNamespace>GlrBridge</RootNamespace>
  </PropertyGroup>
  <ItemGroup>
    <Reference Include="BepInEx">
      <HintPath>$(BEPINEX_ROOT)/core/BepInEx.dll</HintPath>
      <Private>false</Private>
    </Reference>
    <Reference Include="UnityEngine.CoreModule">
      <HintPath>$(GAME_MANAGED_ROOT)/UnityEngine.CoreModule.dll</HintPath>
      <Private>false</Private>
    </Reference>
  </ItemGroup>
</Project>
"""


def _bepinex_plugin(package: str) -> str:
    plugin_id = package.replace("_", ".")
    return f'''using System;
using System.Collections.Concurrent;
using System.Threading;
using BepInEx;

namespace GlrBridge
{{
    public readonly struct BoundedCommand
    {{
        public BoundedCommand(string episodeId, long expectedStepId, string name, float value)
        {{
            EpisodeId = episodeId;
            ExpectedStepId = expectedStepId;
            Name = name;
            Value = value;
        }}

        public string EpisodeId {{ get; }}
        public long ExpectedStepId {{ get; }}
        public string Name {{ get; }}
        public float Value {{ get; }}
    }}

    public readonly struct VerifiedPostState
    {{
        public VerifiedPostState(string episodeId, long stepId)
        {{
            EpisodeId = episodeId;
            StepId = stepId;
        }}

        public string EpisodeId {{ get; }}
        public long StepId {{ get; }}
    }}

    public interface IAuthorizedGameContract
    {{
        bool IsActionAllowed(string name);
        bool TryApply(BoundedCommand command, out VerifiedPostState postState);
    }}

    [BepInPlugin("{plugin_id}.glr", "GLR bounded bridge", "0.1.0")]
    public sealed class GlrBridgePlugin : BaseUnityPlugin
    {{
        private const int MaxPendingCommands = 64;
        private readonly ConcurrentQueue<BoundedCommand> pending = new();
        private IAuthorizedGameContract? gameContract;
        private int pendingCount;
        private string episodeId = string.Empty;
        private long stepId;

        public void Bind(IAuthorizedGameContract contract, string authorizedEpisodeId)
        {{
            gameContract = contract ?? throw new ArgumentNullException(nameof(contract));
            episodeId = string.IsNullOrWhiteSpace(authorizedEpisodeId)
                ? throw new ArgumentException("episode id is required", nameof(authorizedEpisodeId))
                : authorizedEpisodeId;
            stepId = 0;
        }}

        public bool TryEnqueue(BoundedCommand command)
        {{
            var contract = gameContract;
            if (contract is null || command.EpisodeId != episodeId ||
                command.ExpectedStepId != stepId || !contract.IsActionAllowed(command.Name))
            {{
                return false;
            }}
            if (Interlocked.Increment(ref pendingCount) > MaxPendingCommands)
            {{
                Interlocked.Decrement(ref pendingCount);
                return false;
            }}
            pending.Enqueue(command);
            return true;
        }}

        private void Update()
        {{
            while (pending.TryDequeue(out var command))
            {{
                Interlocked.Decrement(ref pendingCount);
                var contract = gameContract;
                if (contract is null || command.EpisodeId != episodeId ||
                    command.ExpectedStepId != stepId)
                {{
                    continue;
                }}
                if (contract.TryApply(command, out var postState) &&
                    postState.EpisodeId == episodeId && postState.StepId == stepId + 1)
                {{
                    stepId = postState.StepId;
                }}
            }}
        }}
    }}
}}
'''


def _ue4ss_plugin() -> str:
    return """local current_episode = nil
local current_step = 0
local pending = {}
local max_pending_commands = 64

-- Replace this table with reviewed, game-semantic handlers. Unknown names fail closed.
local action_handlers = {}

local function validate_command(command)
    return type(command) == "table"
        and type(command.episode_id) == "string"
        and command.episode_id == current_episode
        and type(command.expected_step_id) == "number"
        and command.expected_step_id == current_step
        and type(command.name) == "string"
        and action_handlers[command.name] ~= nil
end

function GLR_BindAuthorizedEpisode(episode_id)
    if type(episode_id) ~= "string" or episode_id == "" then
        return false
    end
    current_episode = episode_id
    current_step = 0
    pending = {}
    return true
end

function GLR_TryEnqueue(command)
    if #pending >= max_pending_commands or not validate_command(command) then
        return false
    end
    table.insert(pending, command)
    ExecuteInGameThread(function()
        local next_command = table.remove(pending, 1)
        if next_command == nil or not validate_command(next_command) then
            return
        end
        local verified_step = action_handlers[next_command.name](next_command)
        if verified_step == current_step + 1 then
            current_step = verified_step
        end
    end)
    return true
end
"""


def _reference_training_script(package: str, environment_id: str) -> str:
    return f'''"""Deterministic synthetic BC smoke test and reproducible bundle builder."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

import numpy as np
from game_learning_runtime import (
    DemonstrationGate,
    DemonstrationOrigin,
    DemonstrationOutcome,
    DemonstrationProvenance,
    EpisodeRewardGuard,
    SyncCollector,
    build_model_bundle,
    load_demonstration_policy_config,
    load_reward_safety_config,
    load_training_config,
)
from game_learning_runtime.project import find_project

from {package}.environment import create_environment, synthetic_policy

ROOT = find_project(__file__).parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    config = load_training_config(ROOT / "training.json")
    EpisodeRewardGuard(config, load_reward_safety_config(ROOT / "reward-safety.json"))
    demonstration_gate = DemonstrationGate(
        load_demonstration_policy_config(ROOT / "demonstration-policy.json")
    )
    demonstration = demonstration_gate.validate(
        DemonstrationProvenance(
            origin=DemonstrationOrigin.SCRIPTED_EXPERT,
            outcome=DemonstrationOutcome.SUCCESS,
        )
    )
    environment = create_environment()
    try:
        collector = SyncCollector(environment, start_mode=config.lifecycle.start_mode)
        unroll = collector.collect(
            synthetic_policy,
            steps=3,
            seed=7 if config.lifecycle.start_mode == "reset" else None,
            stop_on_done=True,
        )
        choices = [int(transition.action["choice"][0]) for transition in unroll.transitions]
        learned_choice = max(set(choices), key=lambda choice: (choices.count(choice), choice))
        protocol_version = environment.spec.protocol_version
    finally:
        environment.close()

    with tempfile.TemporaryDirectory() as temporary:
        temporary_root = Path(temporary)
        model = temporary_root / "model.json"
        metrics = temporary_root / "metrics.json"
        model.write_text(
            json.dumps(
                {{
                    "schema_version": "glr.reference-policy.v1",
                    "environment_id": "{environment_id}",
                    "action": {{"choice": [learned_choice]}},
                    "learner_seed": 7,
                }},
                indent=2,
            )
            + "\\n",
            encoding="utf-8",
        )
        metrics.write_text(
            json.dumps(
                {{
                    "transition_count": len(unroll.transitions),
                    "total_reward": float(unroll.total_reward.item()),
                    "demonstration_origin": DemonstrationOrigin.SCRIPTED_EXPERT.value,
                    "demonstration_outcome": DemonstrationOutcome.SUCCESS.value,
                    "sample_weight": demonstration.sample_weight,
                }},
                indent=2,
            )
            + "\\n",
            encoding="utf-8",
        )
        input_candidates = {{
            "training.json": ROOT / "training.json",
            "reward-safety.json": ROOT / "reward-safety.json",
            "demonstration-policy.json": ROOT / "demonstration-policy.json",
            "runtime-integration.json": ROOT / "runtime-integration.json",
            "agent-interface.json": ROOT / "agent-interface.json",
            "deployment/loader.json": ROOT / "deployment/loader.json",
            "pyproject.toml": ROOT / "pyproject.toml",
            "vx.toml": ROOT / "vx.toml",
            "uv.lock": ROOT / "uv.lock",
            "src/{package}/environment.py": ROOT / "src/{package}/environment.py",
            "scripts/train_reference.py": ROOT / "scripts/train_reference.py",
            "runtime/bepinex/GlrBridge.csproj": ROOT / "runtime/bepinex/GlrBridge.csproj",
            "runtime/bepinex/GlrBridgePlugin.cs": ROOT / "runtime/bepinex/GlrBridgePlugin.cs",
            "runtime/ue4ss/GLRBridge/Scripts/main.lua": ROOT
            / "runtime/ue4ss/GLRBridge/Scripts/main.lua",
        }}
        build_model_bundle(
            output,
            environment_id="{environment_id}",
            protocol_version=protocol_version,
            algorithm="behavior-cloning-majority",
            framework="numpy",
            framework_version=np.__version__,
            seeds=(7,),
            inputs={{name: path for name, path in input_candidates.items() if path.is_file()}},
            artifacts={{"model.json": model, "metrics.json": metrics}},
        )
    print(f"Created verified model bundle at {{output}}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def _verify_bundle_script() -> str:
    return """from __future__ import annotations

import argparse

from game_learning_runtime import verify_model_bundle


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle")
    args = parser.parse_args()
    manifest = verify_model_bundle(args.bundle)
    print(
        f"Verified {len(manifest.inputs)} inputs and "
        f"{len(manifest.artifacts)} artifacts for {manifest.environment_id}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""


def _glr_role_script() -> str:
    return '''"""Single generated process entrypoint for GLR-owned lifecycle roles."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from game_learning_runtime.project import find_project

ROOT = find_project(__file__).parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("role", choices=("runtime", "trainer", "player"))
    parser.add_argument("value", nargs="?")
    args = parser.parse_args()
    if args.role == "runtime":
        # Synthetic scaffold: real adapters replace this with their reviewed bridge.
        print("synthetic runtime boundary ready")
        return 0
    if args.role == "trainer":
        return subprocess.call(
            [sys.executable, str(ROOT / "scripts/train_reference.py"),
             "--output", str(Path(os.environ["GLR_RUN_DIR"]) / "model-bundle")],
            cwd=ROOT,
        )
    if not args.value:
        parser.error("player requires the verified model bundle path from GLR")
    from game_learning_runtime import verify_model_bundle
    verify_model_bundle(args.value)
    print(f"verified playback bundle {args.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def _glr_project(package: str, environment_id: str, *, has_runtime: bool) -> dict[str, Any]:
    configs = [
        {"owner": "training", "path": "training.json", "schema_version": "glr.training.v1"},
        {
            "owner": "reward",
            "path": "reward-safety.json",
            "schema_version": "glr.reward-safety.v1",
        },
        {
            "owner": "demonstration",
            "path": "demonstration-policy.json",
            "schema_version": "glr.demonstration-policy.v1",
        },
    ]
    if has_runtime:
        configs.append(
            {
                "owner": "runtime",
                "path": "runtime-integration.json",
                "schema_version": "glr.runtime-integration.v1",
            }
        )
    return {
        "schema_version": "glr.project.v1",
        "environment_id": environment_id,
        "environment_family": "synthetic-adapter",
        "protocol_version": "1.0",
        "data_dir": ".glr",
        "bridge_path": f"src/{package}",
        "runtime": {"argv": ["python", "scripts/glr_role.py", "runtime"]},
        "trainer": {"argv": ["python", "scripts/glr_role.py", "trainer"]},
        "player": {"argv": ["python", "scripts/glr_role.py", "player", "{bundle}"]},
        "researcher": None,
        "planner": None,
        "evaluator": None,
        "capture": None,
        "progress": None,
        "lifecycle": {
            "schema_version": "glr.lifecycle.v1",
            "configs": configs,
            "modes": ["train", "frozen-playback"],
        },
    }


def _glr_project_toml(value: dict[str, Any]) -> str:
    """Serialize only the fixed generated project shape, omitting absent roles."""

    lines = [
        f"{key} = {json.dumps(value[key])}"
        for key in (
            "schema_version",
            "environment_id",
            "environment_family",
            "protocol_version",
            "data_dir",
            "bridge_path",
        )
    ]
    for role in ("runtime", "trainer", "player"):
        lines.extend(["", f"[{role}]", f"argv = {json.dumps(value[role]['argv'])}"])
    lifecycle = value["lifecycle"]
    lines.extend(
        [
            "",
            "[lifecycle]",
            f"schema_version = {json.dumps(lifecycle['schema_version'])}",
            f"modes = {json.dumps(lifecycle['modes'])}",
        ]
    )
    for config in lifecycle["configs"]:
        lines.extend(["", "[[lifecycle.configs]]"])
        lines.extend(f"{key} = {json.dumps(item)}" for key, item in config.items())
    return "\n".join(lines) + "\n"


def _package_runtime_script() -> str:
    return """from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path, PurePosixPath

from game_learning_runtime.project import find_project

ROOT = find_project(__file__).parent


def portable_relative(value: object) -> str:
    if not isinstance(value, str) or not value or "\\\\" in value or ":" in value:
        raise ValueError("loader artifact paths must be portable and relative")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("loader artifact paths must be portable and relative")
    return path.as_posix()


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    deployment_path = ROOT / "deployment/loader.json"
    if not deployment_path.is_file():
        raise SystemExit("this adapter lane has no loader deployment manifest")
    deployment = json.loads(deployment_path.read_text(encoding="utf-8"))
    if deployment.get("schema_version") != "glr.loader-deployment.v1":
        raise ValueError("unsupported loader deployment schema")
    if deployment.get("install_mode") != "manual-explicit-target":
        raise ValueError("loader packaging requires manual-explicit-target install mode")
    loader_family = deployment.get("loader_family")
    allowed_layouts = {
        "bepinex": ("runtime/bepinex/", "BepInEx/plugins/"),
        "ue4ss": ("runtime/ue4ss/", "Mods/"),
    }
    if loader_family not in allowed_layouts:
        raise ValueError("unsupported loader family")
    source_prefix, destination_prefix = allowed_layouts[loader_family]

    output = Path(args.output).resolve()
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise FileExistsError(f"loader package output is non-empty: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".{output.name}-", dir=output.parent) as temporary:
        root = Path(temporary)
        files = []
        destinations = set()
        for artifact in deployment.get("artifacts", []):
            source_name = portable_relative(artifact.get("source"))
            destination_name = portable_relative(artifact.get("destination"))
            if not source_name.startswith(source_prefix):
                raise ValueError("loader package source is outside its runtime template")
            if not destination_name.startswith(destination_prefix):
                raise ValueError("loader package destination is outside its plugin directory")
            if destination_name in destinations:
                raise ValueError(f"duplicate loader destination: {destination_name}")
            destinations.add(destination_name)
            source = ROOT / PurePosixPath(source_name)
            if source.is_symlink() or not source.is_file():
                raise FileNotFoundError(f"build loader artifact first: {source_name}")
            destination = root / "payload" / PurePosixPath(destination_name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            files.append(
                {
                    "path": destination_name,
                    "sha256": digest(destination),
                    "size_bytes": destination.stat().st_size,
                }
            )
        if not files:
            raise ValueError("loader deployment must contain at least one artifact")
        manifest = {
            "schema_version": "glr.loader-package.v1",
            "loader_family": loader_family,
            "upstream_version": deployment.get("upstream_version"),
            "install_mode": deployment.get("install_mode"),
            "files": files,
        }
        (root / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\\n", encoding="utf-8", newline="\\n"
        )
        if output.exists():
            output.rmdir()
        root.replace(output)
    print(f"Staged loader package at {output}; installation still requires an explicit target")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="new or empty output directory")
    parser.add_argument("--package", required=True, help="lowercase Python package name")
    parser.add_argument("--environment-id", required=True, help="generic public ID")
    parser.add_argument("--engine", choices=("unity", "unreal", "godot", "other"), default="other")
    parser.add_argument("--unity-runtime", choices=("mono", "il2cpp"))
    parser.add_argument(
        "--access",
        choices=("source", "loader", "external"),
        help="source plugin, authorized loader plugin, or external integration",
    )
    parser.add_argument("--loader", choices=("bepinex", "ue4ss"))
    parser.add_argument("--loader-version", help="exact compatible upstream release tag")
    parser.add_argument("--start-mode", choices=("reset", "attach"))
    args = parser.parse_args()
    if args.unity_runtime is not None and args.engine != "unity":
        parser.error("--unity-runtime requires --engine unity")
    if args.access == "loader" and args.unity_runtime == "il2cpp":
        parser.error("IL2CPP loader bootstrap is not implemented; use source or external access")
    if _PACKAGE.fullmatch(args.package) is None:
        parser.error("--package must match ^[a-z][a-z0-9_]*$")
    if _ENVIRONMENT_ID.fullmatch(args.environment_id) is None:
        parser.error("--environment-id must be a generic identifier without paths or endpoints")
    if args.access is None:
        args.start_mode = args.start_mode or "reset"
    else:
        expected_start = "reset" if args.access == "source" else "attach"
        if args.start_mode is not None and args.start_mode != expected_start:
            parser.error(f"--access {args.access} requires --start-mode {expected_start}")
        args.start_mode = expected_start
    if args.access == "loader":
        if args.loader is None:
            parser.error("--loader is required for --access loader")
        if args.loader_version is None:
            parser.error("--loader-version is required for --access loader")
        if _UPSTREAM_VERSION.fullmatch(args.loader_version) is None:
            parser.error("--loader-version must be a release tag without paths or spaces")
        if args.loader == "bepinex" and args.engine != "unity":
            parser.error("BepInEx requires --engine unity")
        if args.loader == "ue4ss" and args.engine != "unreal":
            parser.error("UE4SS requires --engine unreal")
    elif args.loader is not None or args.loader_version is not None:
        parser.error("--loader and --loader-version require --access loader")
    output = Path(args.output).resolve()
    if output.exists() and any(output.iterdir()):
        parser.error(f"output directory is non-empty and will not be overwritten: {output}")
    args.output = output
    return args


def main() -> int:
    args = _parse_args()
    output: Path = args.output
    output.mkdir(parents=True, exist_ok=True)

    training = _load_asset("training-config.json")
    reward_safety = _load_asset("reward-safety.json")
    demonstration_policy = _load_asset("demonstration-policy.json")
    training["lifecycle"]["start_mode"] = args.start_mode
    if args.access is not None:
        _write(
            output / "runtime-selection.json",
            json.dumps(
                {
                    "engine_family": args.engine,
                    "runtime_variant": args.unity_runtime,
                    "implementation_status": "synthetic-seam",
                    "live_verified": False,
                },
                indent=2,
            )
            + "\n",
        )
        training["bridge"]["required_capabilities"] = _required_capabilities(args.access)
    elif args.start_mode == "attach":
        training["bridge"]["required_capabilities"] = [
            "authenticated",
            "live-attach",
            "postcondition-verified",
            "target-bound",
        ]
    research = _load_asset("knowledge-research.json")
    research["environment_id"] = args.environment_id
    research["generated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    _write(output / "training.json", json.dumps(training, indent=2) + "\n")
    _write(
        output / "reward-safety.json",
        json.dumps(reward_safety, indent=2) + "\n",
    )
    _write(
        output / "demonstration-policy.json",
        json.dumps(demonstration_policy, indent=2) + "\n",
    )
    if args.access is not None:
        _write(
            output / "runtime-integration.json",
            json.dumps(_runtime_integration(args.engine, args.access, loader=args.loader), indent=2)
            + "\n",
        )
    if args.access == "loader":
        _write(
            output / "deployment/loader.json",
            json.dumps(_loader_deployment(args.engine, args.loader, args.loader_version), indent=2)
            + "\n",
        )
        if args.loader == "bepinex":
            _write(output / "runtime/bepinex/GlrBridge.csproj", _bepinex_project())
            _write(
                output / "runtime/bepinex/GlrBridgePlugin.cs",
                _bepinex_plugin(args.package),
            )
        else:
            _write(
                output / "runtime/ue4ss/GLRBridge/Scripts/main.lua",
                _ue4ss_plugin(),
            )
    _write(
        output / "knowledge/research-manifest.json",
        json.dumps(research, indent=2) + "\n",
    )
    _write(output / f"src/{args.package}/__init__.py", "")
    _write(
        output / f"src/{args.package}/environment.py",
        _environment_module(args.start_mode),
    )
    _write(output / "tests/test_adapter_contract.py", _test_module(args.package))
    _write(output / "pyproject.toml", _pyproject(args.package))
    _write(output / "vx.toml", _vx_toml(args.package))
    _write(output / "justfile", _justfile())
    _write(
        output / ".gitignore",
        ".venv-glr/\n.glr/\n__pycache__/\n*.py[cod]\nconfig/*.local.toml\n",
    )
    _write(
        output / "agent-interface.json",
        json.dumps(_agent_interface(args.environment_id, start_mode=args.start_mode), indent=2)
        + "\n",
    )
    _write(output / "AGENTS.md", _agents_md(args.package, loader=args.loader))
    for name, reference in (
        ("QUALITY.md", "downstream-quality.md"),
        ("ARCHITECTURE.md", "module-boundaries.md"),
        ("USER_RELEASE.md", "user-releases.md"),
        ("FRAMEWORK_MIGRATION.md", "framework-migration.md"),
    ):
        _write(output / name, (_SKILL_ROOT / "references" / reference).read_text(encoding="utf-8"))
    _write(
        output / "MIGRATIONS.md",
        _load_text_asset("templates/MIGRATIONS.template.md", package=args.package),
    )
    _write(
        output / "scripts/check_wheel.py",
        _load_text_asset("templates/check_wheel.template.py", package=args.package),
    )
    _write(
        output / "scripts/train_reference.py",
        _reference_training_script(args.package, args.environment_id),
    )
    _write(output / "scripts/verify_bundle.py", _verify_bundle_script())
    _write(output / "scripts/glr_role.py", _glr_role_script())
    _write(
        output / "glr-project.toml",
        _glr_project_toml(
            _glr_project(
                args.package,
                args.environment_id,
                has_runtime=args.access is not None,
            ),
        ),
    )
    _write(output / "scripts/package_runtime.py", _package_runtime_script())
    _write(
        output / "README.md",
        _readme(
            args.package,
            args.environment_id,
            args.start_mode,
            engine=args.engine,
            access=args.access,
            loader=args.loader,
        ),
    )
    print(f"Created synthetic-first GLR adapter lane at {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
