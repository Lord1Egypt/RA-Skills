#!/usr/bin/env python3
"""
Convert Glucose Units
Convert between mmol/L and mg/dL
"""


def mmol_to_mgdl(value_mmol: float) -> float:
    """
    Convert glucose from mmol/L to mg/dL
    
    Args:
        value_mmol: Glucose value in mmol/L
    
    Returns:
        Glucose value in mg/dL
    """
    return value_mmol * 18.018


def mgdl_to_mmol(value_mgdl: float) -> float:
    """
    Convert glucose from mg/dL to mmol/L
    
    Args:
        value_mgdl: Glucose value in mg/dL
    
    Returns:
        Glucose value in mmol/L
    """
    return value_mgdl / 18.018


def convert_glucose(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert glucose value between units
    
    Args:
        value: Glucose value
        from_unit: Source unit ('mmol/L' or 'mg/dL')
        to_unit: Target unit ('mmol/L' or 'mg/dL')
    
    Returns:
        Converted glucose value
    """
    if from_unit == to_unit:
        return value
    
    # Convert to mmol/L first if needed
    if from_unit == 'mg/dL':
        value_mmol = mgdl_to_mmol(value)
    else:
        value_mmol = value
    
    # Convert to target unit
    if to_unit == 'mg/dL':
        return mmol_to_mgdl(value_mmol)
    else:
        return value_mmol


def main():
    """Interactive conversion"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert glucose units')
    parser.add_argument('value', type=float, help='Glucose value to convert')
    parser.add_argument('--from', dest='from_unit', 
                       choices=['mmol/L', 'mg/dL'],
                       required=True,
                       help='Source unit')
    parser.add_argument('--to', dest='to_unit',
                       choices=['mmol/L', 'mg/dL'],
                       required=True,
                       help='Target unit')
    
    args = parser.parse_args()
    
    result = convert_glucose(args.value, args.from_unit, args.to_unit)
    print(f"{args.value} {args.from_unit} = {result:.1f} {args.to_unit}")


if __name__ == "__main__":
    main()
