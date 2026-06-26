"""Shared env helpers for CLI scripts."""

import os


def first_env(*names, default=""):
    for name in names:
        value = os.environ.get(name)
        if value not in (None, ""):
            return value
    return default


def resolve_env_file_from_argv(argv, env_var_name: str = "SORA_ENV_FILE", default_env_file: str = ".env") -> str:
    """Pre-parse --env-file so defaults can use loaded env values."""
    for i, arg in enumerate(argv):
        if arg == "--env-file" and i + 1 < len(argv):
            return argv[i + 1]
        if arg.startswith("--env-file="):
            return arg.split("=", 1)[1]
    return os.environ.get(env_var_name, default_env_file)


def load_env_file(env_file: str) -> str:
    """Load KEY=VALUE .env file without overriding existing process env."""
    if not env_file:
        return ""

    path = os.path.abspath(env_file)
    if not os.path.isfile(path):
        return ""

    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("export "):
                line = line[len("export "):].strip()

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if not key:
                continue

            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('\"', "'"):
                value = value[1:-1]

            os.environ.setdefault(key, value)

    return path
