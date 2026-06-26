# Pharma CSV Pro - Examples

This folder contains example CSV files demonstrating various pharmaceutical data analysis scenarios.

## Example Files

### 1. batch_records.csv
Batch release data for QC testing of finished products.

**Columns:**
- Batch_Number: Unique batch identifier
- Product_Name: Product name and strength
- Manufacturing_Date: Date of manufacture
- Assay: Potency assay result (%)
- Impurity_Total: Total impurities (%)
- Dissolution_30min: Dissolution at 30 minutes (%)
- Hardness_kp: Tablet hardness in kiloponds
- Friability_Percent: Friability test result (%)

**Usage:**
```bash
python3 ../scripts/pharma_analyzer_pro.py batch_records.csv \
    --study-type batch \
    --compliance USP \
    --specs "Assay:95-105,Impurity_Total:<2.0,Dissolution_30min:>75" \
    --detect-oos
```

### 2. stability_study.csv
24-month stability study data with accelerated conditions.

**Columns:**
- Batch_Number: Batch identifier
- Storage_Condition: Storage condition (25C/60RH or 40C/75RH)
- Time_Month: Time point in months
- Assay: Potency assay result (%)
- Impurity_Total: Total impurities (%)
- Water_Content: Water content (%)
- Dissolution_30min: Dissolution at 30 minutes (%)

**Usage:**
```bash
python3 ../scripts/pharma_analyzer_pro.py stability_study.csv \
    --study-type stability \
    --trend-analysis \
    --specs "Assay:90-110,Impurity_Total:<3.0"
```

### 3. method_validation.csv
Method validation data for analytical method qualification.

**Columns:**
- Test_Type: Type of validation test
- Replicate: Replicate number
- Concentration_ug_mL: Nominal concentration
- Peak_Area: Chromatographic peak area
- Calculated_Concentration: Calculated concentration
- Accuracy_Percent: Accuracy result (%)
- Precision_RSD: Precision RSD (%)

**Usage:**
```bash
python3 ../scripts/pharma_analyzer_pro.py method_validation.csv \
    --study-type method-validation \
    --specs "Accuracy_Percent:98-102,Precision_RSD:<2.0"
```

## Expected Results

### Batch Records Analysis
- Should detect B2024006 as OOS for Assay (94.8% < 95%)
- Should detect B2024006 as OOS for Dissolution (76.2% < 75% threshold concern)
- Should detect B2024006 as OOS for Friability (0.75% > 1.0% is OK, but high)
- Process capability should be calculated for numeric columns

### Stability Study Analysis
- Should show decreasing trend for Assay over time
- Should show increasing trend for Impurity over time
- Should predict shelf life based on trend analysis
- Accelerated conditions should show faster degradation

### Method Validation Analysis
- Linearity: R² should be > 0.995
- Accuracy: All levels should be 98-102%
- Precision: RSD should be < 2.0%
