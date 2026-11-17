#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate CyberPPT platform configuration files.

This script checks all YAML configuration files in the agents/ directory
to ensure they conform to the required schema and have consistent structure.
"""

import sys
import io
from pathlib import Path
from typing import Dict, List, Tuple
import yaml

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


REQUIRED_FIELDS = {
    'interface': ['display_name', 'short_description', 'default_prompt', 'skill_type', 'version'],
    'compatibility': ['platforms', 'min_version'],
    'configuration': ['trigger_patterns', 'file_types', 'output_format', 'workflow', 'quality_gates']
}

QUALITY_GATES = [
    'reference_gate', 'evidence_gate', 'storyline_gate', 'density_gate',
    'style_gate', 'blueprint_gate', 'asset_admission_gate', 'editable_layer_gate',
    'visual_semantics_gate', 'curve_trace_gate', 'spatial_registration_gate',
    'container_overflow_gate', 'typography_gate', 'render_qa_gate', 'strict_qa_gate'
]

WORKFLOW_STAGES = ['analysis', 'blueprint', 'reconstruction']


def validate_yaml_structure(config: Dict, platform: str) -> List[str]:
    """Validate the structure of a platform configuration."""
    errors = []
    
    # Check required top-level sections
    for section in REQUIRED_FIELDS.keys():
        if section not in config:
            errors.append(f"Missing required section: {section}")
            continue
            
        # Check required fields in each section
        for field in REQUIRED_FIELDS[section]:
            if field not in config[section]:
                errors.append(f"Missing required field: {section}.{field}")
    
    # Validate quality gates
    if 'configuration' in config and 'quality_gates' in config['configuration']:
        gates = config['configuration']['quality_gates']
        for gate in QUALITY_GATES:
            if gate not in gates:
                errors.append(f"Missing quality gate: {gate}")
    
    # Validate workflow stages
    if 'configuration' in config and 'workflow' in config['configuration']:
        workflow = config['configuration']['workflow']
        if 'stages' in workflow:
            stage_names = [stage['name'] for stage in workflow['stages']]
            for stage in WORKFLOW_STAGES:
                if stage not in stage_names:
                    errors.append(f"Missing workflow stage: {stage}")
    
    # Validate platforms list
    if 'compatibility' in config and 'platforms' in config['compatibility']:
        platforms = config['compatibility']['platforms']
        if platform not in platforms:
            errors.append(f"Platform '{platform}' not in compatibility.platforms list")
    
    return errors


def validate_consistency(configs: Dict[str, Dict]) -> List[str]:
    """Validate consistency across all platform configurations."""
    errors = []
    
    # Get reference config (opencode)
    if 'opencode' not in configs:
        errors.append("Reference platform 'opencode' not found")
        return errors
    
    reference = configs['opencode']
    
    # Check if all platforms have the same number of quality gates
    ref_gates = set(reference['configuration']['quality_gates'])
    for platform, config in configs.items():
        if 'configuration' not in config or 'quality_gates' not in config['configuration']:
            continue
        
        platform_gates = set(config['configuration']['quality_gates'])
        if platform_gates != ref_gates:
            missing = ref_gates - platform_gates
            extra = platform_gates - ref_gates
            if missing:
                errors.append(f"{platform}: Missing quality gates: {missing}")
            if extra:
                errors.append(f"{platform}: Extra quality gates: {extra}")
    
    # Check workflow stages consistency
    ref_stages = [stage['name'] for stage in reference['configuration']['workflow']['stages']]
    for platform, config in configs.items():
        if 'configuration' not in config or 'workflow' not in config['configuration']:
            continue
        
        platform_stages = [stage['name'] for stage in config['configuration']['workflow']['stages']]
        if platform_stages != ref_stages:
            errors.append(f"{platform}: Workflow stages differ from reference: {platform_stages}")
    
    return errors


def main():
    """Main validation function."""
    agents_dir = Path(__file__).parent.parent / 'agents'
    
    if not agents_dir.exists():
        print(f"Error: agents/ directory not found at {agents_dir}")
        sys.exit(1)
    
    yaml_files = list(agents_dir.glob('*.yaml'))
    
    if not yaml_files:
        print("Error: No YAML files found in agents/ directory")
        sys.exit(1)
    
    print(f"Found {len(yaml_files)} platform configuration(s)")
    print("=" * 60)
    
    # Load and validate each config
    configs = {}
    all_errors = {}
    
    for yaml_file in yaml_files:
        platform = yaml_file.stem
        print(f"\nValidating {platform}...")
        
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if config is None:
                print(f"  ❌ Empty configuration file")
                all_errors[platform] = ["Empty configuration file"]
                continue
            
            configs[platform] = config
            
            # Validate structure
            errors = validate_yaml_structure(config, platform)
            
            if errors:
                print(f"  ❌ Found {len(errors)} error(s):")
                for error in errors:
                    print(f"    - {error}")
                all_errors[platform] = errors
            else:
                print(f"  ✅ Configuration structure is valid")
                
                # Print summary
                display_name = config['interface']['display_name']
                version = config['interface']['version']
                platforms = config['compatibility']['platforms']
                gates_count = len(config['configuration']['quality_gates'])
                
                print(f"     Display Name: {display_name}")
                print(f"     Version: {version}")
                print(f"     Platforms: {', '.join(platforms)}")
                print(f"     Quality Gates: {gates_count}/16")
        
        except yaml.YAMLError as e:
            print(f"  ❌ YAML parsing error: {e}")
            all_errors[platform] = [f"YAML parsing error: {e}"]
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            all_errors[platform] = [f"Unexpected error: {e}"]
    
    # Check consistency across platforms
    print("\n" + "=" * 60)
    print("Checking cross-platform consistency...")
    
    if len(configs) > 1:
        consistency_errors = validate_consistency(configs)
        if consistency_errors:
            print("  ❌ Consistency issues found:")
            for error in consistency_errors:
                print(f"    - {error}")
        else:
            print("  ✅ All platforms are consistent")
    else:
        print("  ⚠️  Only one platform config found, skipping consistency check")
    
    # Summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    total_platforms = len(yaml_files)
    valid_platforms = total_platforms - len(all_errors)
    
    print(f"Total Platforms: {total_platforms}")
    print(f"Valid: {valid_platforms}")
    print(f"Invalid: {len(all_errors)}")
    
    if all_errors:
        print("\n❌ Validation failed for some platforms")
        print("Please fix the errors above and run validation again")
        sys.exit(1)
    else:
        print("\n✅ All platform configurations are valid!")
        sys.exit(0)


if __name__ == '__main__':
    main()
