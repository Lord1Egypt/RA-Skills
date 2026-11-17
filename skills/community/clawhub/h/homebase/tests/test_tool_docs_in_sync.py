"""
test_tool_docs_in_sync.py — the dispatch table and the agent reference must agree.

`SKILL.md` tells the agent: "Full per-tool reference: {baseDir}/references/agent.md
— read it when you need a tool's exact arguments or a flow you have not run
before." When a tool is missing from that file, an agent sent there for exact
arguments finds nothing and improvises.

It had drifted: 15 of 57 tools were undocumented, including every tool in the
evening-brief, travel-mode and bills paths — the three newest and least
guessable features. `agent.md` had also gone actively wrong, telling the agent
that "there is no dedicated range tool" and to read
`calendar_data/family_calendar.json` by hand, long after `get_events_for_range`
existed.

Docs drift silently and code does not, so this asserts the direction that
matters: every dispatchable tool is named in the reference.
"""

import ast
import os
import re

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_PY = os.path.join(SKILL_DIR, "tools.py")
AGENT_MD = os.path.join(SKILL_DIR, "references", "agent.md")


def dispatch_tool_names():
    """Every key of every dict literal assigned or .update()-ed inside
    execute_tool — i.e. every name the agent can actually call."""
    tree = ast.parse(open(TOOLS_PY).read(), filename=TOOLS_PY)
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "execute_tool")
    names = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Dict):
            for key in node.keys:
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    names.add(key.value)
    return names


def documented_tool_names():
    """Tool names merely MENTIONED in agent.md, as `backticked` identifiers.

    Deliberately loose, and used only for the phantom direction. It admits any
    backticked lowercase word, including non-tools like `count` and `status`.
    """
    text = open(AGENT_MD).read()
    return set(re.findall(r"`([a-z_][a-z0-9_]{3,})`", text))


def documented_with_args():
    """Tools agent.md actually SPECIFIES, i.e. gives an `— args:` entry.

    This is the property the forward test needs. SKILL.md sends the agent here
    for "a tool's exact arguments"; a name appearing somewhere in prose does
    not deliver that, so the looser sweep above was satisfiable by
    name-dropping and 7 dispatchable tools passed it with no entry of their own.
    """
    text = open(AGENT_MD).read()
    return set(re.findall(r"`([a-z_][a-z0-9_]{3,})`\s+—\s+args:", text))


class TestToolDocsInSync:
    def test_every_dispatchable_tool_is_documented(self):
        dispatched = dispatch_tool_names()
        documented = documented_with_args()
        missing = sorted(dispatched - documented)
        assert not missing, (
            f"{len(missing)} tool(s) are callable but absent from "
            "references/agent.md, which SKILL.md calls the full per-tool "
            "reference. Document them there:\n  " + "\n  ".join(missing)
        )

    def test_documented_tools_all_exist(self):
        """The other direction: agent.md must not describe a tool that was
        deleted. `sync_school_calendar` sat in both for months as a no-op that
        only ever returned '⚠️ This tool is deprecated.'"""
        dispatched = dispatch_tool_names()
        module = ast.parse(open(TOOLS_PY).read())
        defined = {n.name for n in module.body if isinstance(n, ast.FunctionDef)}

        # Only check names that look like they're being presented as tools:
        # documented, and defined nowhere in tools.py, and not dispatchable.
        text = open(AGENT_MD).read()
        claimed = {
            name for name in documented_tool_names()
            if re.search(rf"`{name}` — args:", text)
        }
        # NOT `- defined`: a tool removed from the dispatch table but left
        # defined in tools.py is exactly the sync_school_calendar case this
        # test cites, and subtracting `defined` excused it. What matters to an
        # agent reading agent.md is whether it can CALL the thing.
        phantom = sorted(claimed - dispatched)
        assert not phantom, (
            "references/agent.md documents tool(s) that are not dispatchable:\n  "
            + "\n  ".join(phantom)
        )

    def test_the_dispatch_parser_actually_finds_tools(self):
        """A guard whose parser silently returns nothing always passes."""
        names = dispatch_tool_names()
        assert len(names) > 40, f"only found {len(names)} tools — parser broke"
        assert "get_morning_briefing" in names
        # Was `add_calendar_event` until 2026-09-07, when calendar writes moved
        # to the gog CLI and that tool was deleted. Canaries have to be tools
        # that will still be here, so this one is a household concern rather
        # than a Google one.
        assert "get_grocery_list" in names
