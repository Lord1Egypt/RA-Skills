"""Registry of exposed cloud functions. Add new entries here when scaffolding a function."""
from functions.hello_world import hello_world

EXPOSED_FUNCTIONS = {
    "hello_world": hello_world,
}
