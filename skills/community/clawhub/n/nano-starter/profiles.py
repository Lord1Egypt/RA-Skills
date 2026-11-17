"""Profiles: which tools this install registers, decided once, at startup.

The whole value of `receive-only` is that an operator can read the MCP
tool list and see that nothing in it can move money out. That only holds
if the profile is enforced HERE, in the server, rather than by the
absence of an environment variable:

  * `send` is not registered at all in `receive-only`. It is absent from
    `tools/list`, and calling it is -32601 method not found, because the
    method genuinely does not exist. Not a 403 - a 403 tells an operator
    the capability is present and merely switched off.

  * `--profile receive-only` together with NANO_WALLET_ALLOW_SEND=1 is a
    startup failure, exit 2. A profile a stray environment variable can
    widen is not a profile, and an operator who approved a receive-only
    scope would never see the widening.

Everything else in the package reads the tool list from here, so the
capability document and the selfcheck cannot drift from what the server
actually serves.
"""

RECEIVE_ONLY = "receive-only"
FULL = "full"

#: The exact tool set of each profile, in the order `tools/list` returns them.
PROFILE_TOOLS = {
    RECEIVE_ONLY: ("create_address", "validate_address", "balance", "receive"),
    FULL: ("create_address", "validate_address", "balance", "receive", "send",
           # The whole nano-wallet 1.0.0 surface, retained unchanged so an install
           # that already speaks these names keeps working. They are offline pure
           # functions with no spend capability, and like everything else outside
           # its four tools they are absent from receive-only.
           "nano_validate_address", "nano_create_wallet",
           "nano_derive_account", "nano_sign_message"),
}

#: Tools that can move money. Never registered in a receive-only install.
SPEND_TOOLS = frozenset({"send"})

PROFILE_NAMES = tuple(sorted(PROFILE_TOOLS))
DEFAULT_PROFILE = FULL

EXIT_PROFILE_ERROR = 2

WIDENING_MESSAGE = (
    "receive-only profile cannot be combined with send authority; "
    "drop --profile receive-only to enable sending"
)


class ProfileError(Exception):
    """A configuration this install refuses to start under.

    Always exit(2) on this: the process must never go on to serve a
    request under a configuration it could not make sense of.
    """

    def __init__(self, reason: str, message: str):
        super().__init__(message)
        self.reason = reason
        self.message = message
        self.exit_code = EXIT_PROFILE_ERROR


def resolve(name, env=None) -> str:
    """Validate a profile name against the environment, or raise ProfileError.

    This is the startup gate. Call it before binding anything.
    """
    import os
    env = os.environ if env is None else env
    name = (name or env.get("NANO_WALLET_PROFILE") or DEFAULT_PROFILE).strip()
    if name not in PROFILE_TOOLS:
        raise ProfileError(
            "unknown_profile",
            "unknown profile %r; known profiles: %s" % (name, ", ".join(PROFILE_NAMES)),
        )
    if name == RECEIVE_ONLY and str(env.get("NANO_WALLET_ALLOW_SEND", "")).strip() == "1":
        raise ProfileError("profile_widened", WIDENING_MESSAGE)
    return name


def tools_for(name: str) -> tuple:
    return PROFILE_TOOLS[name]


def registers_spend(name: str) -> bool:
    return bool(SPEND_TOOLS & set(PROFILE_TOOLS[name]))


def ambient(env=None, requested=None) -> str:
    """The profile this INSTALL is configured to run under.

    NANO_WALLET_PROFILE wins, because that is what the operator's
    `mcp.json` sets and what the server will actually use. A `--profile`
    argument names the profile being asked about; when the environment is
    silent it is also the one the install would run under.

    The distinction is what lets `selfcheck --profile receive-only` fail
    honestly on an install configured for `full`, instead of checking a
    hypothetical.
    """
    import os
    env = os.environ if env is None else env
    return (env.get("NANO_WALLET_PROFILE") or requested or DEFAULT_PROFILE).strip()
