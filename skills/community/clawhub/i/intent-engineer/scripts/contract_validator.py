#!/usr/bin/env python3
"""
Data Contract Validator: Validates data against JSON Schema contracts.

This utility helps ensure data flowing between skills conforms to defined contracts.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Tuple, List
import jsonschema


class ContractValidator:
    """Validates data against data contract schemas."""

    def __init__(self, contracts_dir: str = "references"):
        """Initialize with path to contracts directory."""
        self.contracts_dir = Path(contracts_dir)
        self.contracts: Dict[str, Dict[str, Any]] = {}
        self._load_contracts()

    def _load_contracts(self) -> None:
        """Load all contract schemas from the contracts directory."""
        for contract_file in self.contracts_dir.glob("data_contracts_*.json"):
            contract_id = contract_file.stem.replace("data_contracts_", "")
            try:
                with open(contract_file, 'r') as f:
                    self.contracts[contract_id] = json.load(f)
                print(f"✓ Loaded contract: {contract_id}")
            except Exception as e:
                print(f"✗ Failed to load contract {contract_id}: {e}")

    def validate(self, data: Dict[str, Any], contract_id: str) -> Tuple[bool, List[str]]:
        """
        Validate data against a contract.

        Args:
            data: Data to validate
            contract_id: ID of the contract to validate against

        Returns:
            (is_valid, error_messages)
        """
        if contract_id not in self.contracts:
            return False, [f"Contract not found: {contract_id}"]

        contract = self.contracts[contract_id]
        errors = []

        try:
            jsonschema.validate(data, contract)
            return True, []
        except jsonschema.ValidationError as e:
            errors.append(f"Validation error: {e.message}")
            return False, errors
        except jsonschema.SchemaError as e:
            errors.append(f"Schema error: {e.message}")
            return False, errors

    def validate_file(self, data_file: str, contract_id: str) -> Tuple[bool, List[str]]:
        """
        Validate data from a JSON file against a contract.

        Args:
            data_file: Path to JSON file containing data
            contract_id: ID of the contract to validate against

        Returns:
            (is_valid, error_messages)
        """
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            return self.validate(data, contract_id)
        except Exception as e:
            return False, [f"Failed to load data file: {e}"]

    def list_contracts(self) -> None:
        """List all available contracts."""
        print("\nAvailable Contracts:")
        print("-" * 50)
        for contract_id, contract in self.contracts.items():
            title = contract.get('title', 'Untitled')
            description = contract.get('description', '')
            print(f"\n{contract_id}")
            print(f"  Title: {title}")
            print(f"  Description: {description}")
            print(f"  Properties: {', '.join(contract.get('properties', {}).keys())}")

    def get_contract_schema(self, contract_id: str) -> Dict[str, Any]:
        """Get the schema for a contract."""
        return self.contracts.get(contract_id, {})


def main():
    """CLI interface for contract validation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate data against data contract schemas"
    )
    parser.add_argument(
        '--contracts-dir',
        default='references',
        help='Directory containing contract schemas'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available contracts'
    )
    parser.add_argument(
        '--validate',
        nargs=2,
        metavar=('DATA_FILE', 'CONTRACT_ID'),
        help='Validate a data file against a contract'
    )
    parser.add_argument(
        '--schema',
        metavar='CONTRACT_ID',
        help='Print the schema for a contract'
    )

    args = parser.parse_args()

    validator = ContractValidator(args.contracts_dir)

    if args.list:
        validator.list_contracts()
    elif args.validate:
        data_file, contract_id = args.validate
        is_valid, errors = validator.validate_file(data_file, contract_id)
        if is_valid:
            print(f"✓ Data is valid against contract '{contract_id}'")
            sys.exit(0)
        else:
            print(f"✗ Data validation failed:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
    elif args.schema:
        schema = validator.get_contract_schema(args.schema)
        if schema:
            print(json.dumps(schema, indent=2))
        else:
            print(f"Contract not found: {args.schema}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
