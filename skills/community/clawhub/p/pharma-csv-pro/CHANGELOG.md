# Changelog

## v1.0.0 (2026-03-07)

### Initial Release

#### Core Features
- **Data Validation**: Missing value detection, duplicate checking, outlier detection using IQR method
- **Statistical Analysis**: Descriptive statistics, Cpk/Ppk process capability, control chart metrics
- **OOS/OOT Detection**: Out-of-specification and out-of-trend flagging with configurable limits
- **Trend Analysis**: Linear regression for stability studies with shelf-life prediction
- **Compliance Checking**: USP/EP/ChP standard validation

#### Supported Study Types
- Batch record analysis
- Stability studies (ICH guidelines)
- Method validation
- General pharmaceutical data

#### Output Formats
- Markdown (human-readable reports)
- JSON (machine-readable for integration)

#### Example Datasets
- Batch records (20 batches, 2 products)
- Stability study (36 time points, 2 storage conditions)
- Method validation (linearity, accuracy, precision)

#### Documentation
- SKILL.md with usage instructions
- Regulatory standards reference
- Advanced usage guide with LIMS integration examples
- Example datasets with README
