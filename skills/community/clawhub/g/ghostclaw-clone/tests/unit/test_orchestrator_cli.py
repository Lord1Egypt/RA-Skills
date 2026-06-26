"""Tests for orchestrator CLI flags parsing and overrides."""

import pytest
from argparse import Namespace, ArgumentParser
from ghostclaw.cli.commands.analyze import AnalyzeCommand


class TestOrchestrateCLI:
    """Test that --orchestrate and --no-orchestrate flags are converted to config overrides."""

    def test_orchestrate_flag_sets_override(self):
        """--orchestrate should result in overrides['orchestrate']=True."""
        cmd = AnalyzeCommand()
        args = Namespace(
            orchestrate=True,
            no_orchestrate=False,
            use_ai=None, no_ai=None, ai_provider=None, ai_model=None,
            dry_run=None, verbose=None, patch=None, delta=None, delta_base_ref=None,
            use_qmd=None, embedding_backend=None,
            pyscn=None, no_pyscn=None, ai_codeindex=None, no_ai_codeindex=None,
            no_parallel=None, concurrency_limit=None
        )
        overrides = cmd._build_cli_overrides(args)
        assert overrides.get("orchestrate") is True

    def test_no_orchestrate_flag_sets_override_false(self):
        """--no-orchestrate should result in overrides['orchestrate']=False."""
        cmd = AnalyzeCommand()
        args = Namespace(
            orchestrate=False,
            no_orchestrate=True,
            use_ai=None, no_ai=None, ai_provider=None, ai_model=None,
            dry_run=None, verbose=None, patch=None, delta=None, delta_base_ref=None,
            use_qmd=None, embedding_backend=None,
            pyscn=None, no_pyscn=None, ai_codeindex=None, no_ai_codeindex=None,
            no_parallel=None, concurrency_limit=None
        )
        overrides = cmd._build_cli_overrides(args)
        assert overrides.get("orchestrate") is False

    def test_absent_orchestrate_flag_not_in_overrides(self):
        """When neither --orchestrate nor --no-orchestrate is used, 'orchestrate' should not be in overrides."""
        cmd = AnalyzeCommand()
        args = Namespace(
            orchestrate=False,
            no_orchestrate=False,
            use_ai=None, no_ai=None, ai_provider=None, ai_model=None,
            dry_run=None, verbose=None, patch=None, delta=None, delta_base_ref=None,
            use_qmd=None, embedding_backend=None,
            pyscn=None, no_pyscn=None, ai_codeindex=None, no_ai_codeindex=None,
            no_parallel=None, concurrency_limit=None
        )
        overrides = cmd._build_cli_overrides(args)
        assert "orchestrate" not in overrides

    def test_orchestrate_flag_with_other_flags(self):
        """Orchestrate should coexist with other overrides."""
        cmd = AnalyzeCommand()
        args = Namespace(
            orchestrate=True,
            no_orchestrate=False,
            use_ai=True, no_ai=False, ai_provider=None, ai_model=None,
            dry_run=False, verbose=True, patch=False, delta=False, delta_base_ref=None,
            use_qmd=True, embedding_backend=None,
            pyscn=False, no_pyscn=False, ai_codeindex=None, no_ai_codeindex=False,
            no_parallel=False, concurrency_limit=16
        )
        overrides = cmd._build_cli_overrides(args)
        assert overrides["orchestrate"] is True
        assert overrides.get("use_ai") is True
        assert overrides.get("use_qmd") is True
        assert overrides.get("verbose") is True
        assert overrides.get("concurrency_limit") == 16


class TestOrchestrateCLIParser:
    """Test that argparse is configured correctly for --orchestrate/--no-orchestrate."""

    def _make_parser(self):
        cmd = AnalyzeCommand()
        parser = ArgumentParser()
        cmd.configure_parser(parser)
        return parser

    def test_orchestrate_flag_registered_in_parser(self):
        """Parser should accept --orchestrate without error."""
        parser = self._make_parser()
        args = parser.parse_args(["--orchestrate"])
        assert args.orchestrate is True
        assert args.no_orchestrate is False

    def test_no_orchestrate_flag_registered_in_parser(self):
        """Parser should accept --no-orchestrate without error."""
        parser = self._make_parser()
        args = parser.parse_args(["--no-orchestrate"])
        assert args.no_orchestrate is True
        assert args.orchestrate is False

    def test_orchestrate_and_no_orchestrate_are_mutually_exclusive(self):
        """--orchestrate and --no-orchestrate must be mutually exclusive."""
        parser = self._make_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["--orchestrate", "--no-orchestrate"])

    def test_neither_flag_gives_false_defaults(self):
        """Omitting both flags means both are False by default (store_true default)."""
        parser = self._make_parser()
        args = parser.parse_args([])
        assert args.orchestrate is False
        assert args.no_orchestrate is False

    def test_orchestrate_override_value_is_strict_bool_true(self):
        """The override value stored must be exactly True (bool), not just truthy."""
        cmd = AnalyzeCommand()
        args = Namespace(
            orchestrate=True, no_orchestrate=False,
            use_ai=None, no_ai=None, ai_provider=None, ai_model=None,
            dry_run=None, verbose=None, patch=None, delta=None, delta_base_ref=None,
            use_qmd=None, embedding_backend=None,
            pyscn=None, no_pyscn=None, ai_codeindex=None, no_ai_codeindex=None,
            no_parallel=None, concurrency_limit=None
        )
        overrides = cmd._build_cli_overrides(args)
        assert type(overrides["orchestrate"]) is bool
        assert overrides["orchestrate"] is True

    def test_no_orchestrate_override_value_is_strict_bool_false(self):
        """The override value stored when using --no-orchestrate must be exactly False (bool)."""
        cmd = AnalyzeCommand()
        args = Namespace(
            orchestrate=False, no_orchestrate=True,
            use_ai=None, no_ai=None, ai_provider=None, ai_model=None,
            dry_run=None, verbose=None, patch=None, delta=None, delta_base_ref=None,
            use_qmd=None, embedding_backend=None,
            pyscn=None, no_pyscn=None, ai_codeindex=None, no_ai_codeindex=None,
            no_parallel=None, concurrency_limit=None
        )
        overrides = cmd._build_cli_overrides(args)
        assert type(overrides["orchestrate"]) is bool
        assert overrides["orchestrate"] is False

    def test_orchestrate_only_sets_orchestrate_key(self):
        """Using --orchestrate should not inject any unexpected keys beyond 'orchestrate'."""
        cmd = AnalyzeCommand()
        args = Namespace(
            orchestrate=True, no_orchestrate=False,
            use_ai=None, no_ai=None, ai_provider=None, ai_model=None,
            dry_run=None, verbose=None, patch=None, delta=None, delta_base_ref=None,
            use_qmd=None, embedding_backend=None,
            pyscn=None, no_pyscn=None, ai_codeindex=None, no_ai_codeindex=None,
            no_parallel=None, concurrency_limit=None
        )
        overrides = cmd._build_cli_overrides(args)
        assert overrides == {"orchestrate": True}

    def test_no_orchestrate_only_sets_orchestrate_key(self):
        """Using --no-orchestrate should not inject any unexpected keys beyond 'orchestrate'."""
        cmd = AnalyzeCommand()
        args = Namespace(
            orchestrate=False, no_orchestrate=True,
            use_ai=None, no_ai=None, ai_provider=None, ai_model=None,
            dry_run=None, verbose=None, patch=None, delta=None, delta_base_ref=None,
            use_qmd=None, embedding_backend=None,
            pyscn=None, no_pyscn=None, ai_codeindex=None, no_ai_codeindex=None,
            no_parallel=None, concurrency_limit=None
        )
        overrides = cmd._build_cli_overrides(args)
        assert overrides == {"orchestrate": False}

    def test_orchestrate_does_not_affect_parallel_or_concurrency_keys(self):
        """Setting --orchestrate should not alter parallel_enabled or concurrency_limit."""
        cmd = AnalyzeCommand()
        args = Namespace(
            orchestrate=True, no_orchestrate=False,
            use_ai=None, no_ai=None, ai_provider=None, ai_model=None,
            dry_run=None, verbose=None, patch=None, delta=None, delta_base_ref=None,
            use_qmd=None, embedding_backend=None,
            pyscn=None, no_pyscn=None, ai_codeindex=None, no_ai_codeindex=None,
            no_parallel=None, concurrency_limit=None
        )
        overrides = cmd._build_cli_overrides(args)
        assert "parallel_enabled" not in overrides
        assert "concurrency_limit" not in overrides