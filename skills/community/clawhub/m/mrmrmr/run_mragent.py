#!/usr/bin/env python3
"""
MRAgent CLI - Command-line interface for MRAgent Mendelian Randomization analysis
Part of OpenClaw Skill specification
"""

import argparse
import os
import sys
import json
from typing import Optional, Dict, Any

# Add the original MRAgent project to Python path
# If MRAgent is installed globally, this may not be necessary
# but we support both installed and source modes
mragent_source_path = os.environ.get(
    "MRAGENT_SOURCE_PATH",
    os.path.join(os.path.dirname(__file__), "mrmrmr")
)
if os.path.exists(mragent_source_path) and mragent_source_path not in sys.path:
    sys.path.insert(0, mragent_source_path)

# Now import MRAgent
try:
    from mragent.agent_workflow import MRAgent
    from mragent.agent_workflow_OE import MRAgentOE
except ImportError as e:
    print(f"ERROR: Cannot import MRAgent. {e}", file=sys.stderr)
    print("Please ensure MRAgent is installed or MRAGENT_SOURCE_PATH is set correctly.", file=sys.stderr)
    sys.exit(1)


def get_api_keys() -> Dict[str, Optional[str]]:
    """Get API keys from environment variables"""
    return {
        "openai_api_key": os.environ.get("OPENAI_API_KEY"),
        "opengwas_jwt": os.environ.get("OPENGWAS_JWT"),
        "llm_model": os.environ.get("LLM_MODEL", "gpt-4o"),
        "llm_provider": os.environ.get("LLM_PROVIDER", "openai"),
        "base_url": os.environ.get("OPENAI_BASE_URL"),
    }


def main():
    parser = argparse.ArgumentParser(
        description="MRAgent: Automated Mendelian Randomization analysis powered by LLM"
    )

    # Required mode argument
    parser.add_argument(
        "--mode", "-m",
        required=True,
        choices=["KD", "CV", "knowledge-discovery", "causal-validation"],
        help="Operation mode: KD (knowledge-discovery) = discover novel causal pairs from literature; CV (causal-validation) = validate a specific exposure-outcome pair"
    )

    # Outcome (disease) - required for both modes in different ways
    parser.add_argument(
        "--outcome", "-o",
        help="Outcome (disease) to study. Required in KD mode. Required in CV mode."
    )

    # Exposure - required for CV mode
    parser.add_argument(
        "--exposure", "-e",
        help="Exposure factor/risk factor to test. Required in CV mode."
    )

    # Optional parameters
    parser.add_argument(
        "--num-pubmed", "-n",
        type=int,
        default=100,
        help="Number of recent papers to fetch from PubMed (default: 100)"
    )

    parser.add_argument(
        "--model",
        choices=["MR", "MR_MOE"],
        default="MR",
        help="Mendelian Randomization model type: standard MR or Mixture of Experts (default: MR)"
    )

    parser.add_argument(
        "--llm-model",
        help="LLM model name (overrides environment variable LLM_MODEL)"
    )

    parser.add_argument(
        "--bidirectional", "-b",
        action="store_true",
        default=False,
        help="Also perform bidirectional MR analysis (reverse direction: outcome -> exposure)"
    )

    parser.add_argument(
        "--no-synonyms",
        action="store_true",
        default=False,
        help="Disable synonym expansion (faster but less comprehensive)"
    )

    parser.add_argument(
        "--no-introduction",
        action="store_true",
        default=False,
        help="Disable automatic introduction generation"
    )

    parser.add_argument(
        "--strobe-mr",
        action="store_true",
        default=False,
        help="Enable STROBE-MR quality assessment of existing studies"
    )

    parser.add_argument(
        "--mrlap",
        action="store_true",
        default=False,
        help="Enable MRlap sample overlap correction (requires additional R packages)"
    )

    parser.add_argument(
        "--opengwas-mode",
        choices=["online", "csv"],
        default="online",
        help="OpenGWAS query mode: online or local CSV cache (default: online)"
    )

    parser.add_argument(
        "--gwas-source",
        choices=["opengwas", "gwas_catalog", "fingen", "ukbiobank", "all"],
        default="opengwas",
        help="GWAS data source: opengwas (default), gwas_catalog (EMBL-EBI), fingen (FinnGen), ukbiobank (UK Biobank), all (all sources combined)"
    )

    parser.add_argument(
        "--output-dir",
        default="./output",
        help="Root directory for output files (default: ./output)"
    )

    parser.add_argument(
        "--steps",
        help="Specific steps to run (comma-separated, e.g. 1,2,3). Default: run all steps"
    )

    args = parser.parse_args()

    # Get API keys from environment
    keys = get_api_keys()

    # Validate required environment
    if keys["openai_api_key"] is None and keys["llm_provider"] == "openai":
        print(
            "ERROR: OPENAI_API_KEY environment variable is not set.\n"
            "Please set it before running MRAgent:\n"
            "  export OPENAI_API_KEY=your-key-here",
            file=sys.stderr
        )
        sys.exit(1)

    # Normalize mode
    mode_map = {
        "KD": "KD",
        "knowledge-discovery": "KD",
        "CV": "CV",
        "causal-validation": "CV",
    }
    normalized_mode = mode_map[args.mode]

    # Validate required arguments based on mode
    if normalized_mode == "KD" and args.outcome is None:
        print("ERROR: --outcome is required in knowledge discovery (KD) mode", file=sys.stderr)
        sys.exit(1)

    if normalized_mode == "CV" and (args.outcome is None or args.exposure is None):
        print("ERROR: both --outcome and --exposure are required in causal validation (CV) mode", file=sys.stderr)
        sys.exit(1)

    # Parse steps if specified
    steps = None
    if args.steps:
        steps = [int(s.strip()) for s in args.steps.split(",")]

    # Get LLM model
    llm_model = args.llm_model if args.llm_model else keys["llm_model"]

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Run based on mode
    try:
        if normalized_mode == "CV":
            # Causal Validation mode - use MRAgentOE
            agent = MRAgentOE(
                exposure=args.exposure,
                outcome=args.outcome,
                AI_key=keys["openai_api_key"],
                model=args.model,
                num=args.num_pubmed,
                bidirectional=args.bidirectional,
                synonyms=not args.no_synonyms,
                introduction=not args.no_introduction,
                LLM_model=llm_model,
                model_type=keys["llm_provider"],
                base_url=keys["base_url"],
                gwas_token=keys["opengwas_jwt"],
                opengwas_mode=args.opengwas_mode,
                gwas_source=args.gwas_source,
                mr_quality_evaluation=args.strobe_mr,
                mrlap=args.mrlap
            )
        else:
            # Knowledge Discovery mode - use MRAgent with mode='O'
            agent = MRAgent(
                mode='O',
                outcome=args.outcome,
                exposure=args.exposure,
                AI_key=keys["openai_api_key"],
                model=args.model,
                num=args.num_pubmed,
                bidirectional=args.bidirectional,
                synonyms=not args.no_synonyms,
                introduction=not args.no_introduction,
                LLM_model=llm_model,
                model_type=keys["llm_provider"],
                base_url=keys["base_url"],
                gwas_token=keys["opengwas_jwt"],
                opengwas_mode=args.opengwas_mode,
                gwas_source=args.gwas_source,
                mr_quality_evaluation=args.strobe_mr,
                mrlap=args.mrlap
            )

        print(f"[START] MRAgent starting in {normalized_mode} mode")
        print(f"[CONFIG] Output directory: {agent.path}")
        print(f"[CONFIG] LLM model: {llm_model}")

        # Run the analysis
        agent.run(step=steps)

        # Collect and output results
        result = {
            "success": True,
            "mode": normalized_mode,
            "outcome": args.outcome,
            "exposure": args.exposure,
            "output_directory": agent.path,
            "discovered_pairs": None,
            "selected_for_mr": None,
            "reports": []
        }

        # Read discovered pairs
        eo_csv = os.path.join(agent.path, "Exposure_and_Outcome.csv")
        if os.path.exists(eo_csv):
            import pandas as pd
            df = pd.read_csv(eo_csv)
            result["discovered_pairs"] = len(df)
            # Get the unstudied pairs
            if "MRorNot" in df.columns:
                result["unstudied_pairs"] = len(df[df["MRorNot"] != "Yes"])

        # Read selected pairs
        mr_csv = os.path.join(agent.path, "mr_run.csv")
        if os.path.exists(mr_csv):
            import pandas as pd
            df = pd.read_csv(mr_csv)
            result["selected_for_mr"] = len(df)

        # Find generated PDF reports
        # Walk the directory tree to find all Report.pdf files
        if os.path.exists(agent.path):
            for root, dirs, files in os.walk(agent.path):
                for file in files:
                    if file.endswith(".pdf"):
                        result["reports"].append(os.path.join(root, file))

        # Output final result as JSON for easy parsing
        print("\n" + "="*60)
        print("MRAgent ANALYSIS COMPLETE")
        print("="*60 + "\n")
        print(json.dumps(result, indent=2))

        # Also print human-friendly summary
        print(f"\nSummary:")
        print(f"  Mode: {result['mode']}")
        print(f"  Outcome: {result['outcome']}")
        if result['exposure']:
            print(f"  Exposure: {result['exposure']}")
        if result['discovered_pairs'] is not None:
            print(f"  Discovered exposure-outcome pairs: {result['discovered_pairs']}")
        if result['selected_for_mr'] is not None:
            print(f"  Pairs selected for MR analysis: {result['selected_for_mr']}")
        print(f"  Output directory: {result['output_directory']}")
        print(f"  Generated {len(result['reports'])} PDF report(s)")
        for report in result['reports']:
            print(f"    - {report}")

    except Exception as e:
        import traceback
        error_result = {
            "success": False,
            "mode": normalized_mode,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_result, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
