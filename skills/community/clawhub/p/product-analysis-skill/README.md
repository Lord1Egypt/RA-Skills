# LAOSI Product Analysis Skill

AI-powered product analysis skill for OpenClaw agents that analyzes market trends, competitor products, and provides recommendations for product selection and optimization.

## Features

- Market trend analysis
- Competitor product comparison
- Product selection recommendations
- Optimization suggestions
- Batch processing capabilities
- Integration with OpenClaw's SubAgent system for parallel analysis

## Installation

Install via ClawHub:

```bash
clawhub install laosi-product-analysis-skill
```

## Usage

### Basic Usage

```bash
laosi-product-analysis-skill analyze --product "Product Name" --category "Electronics"
```

### Batch Analysis

```bash
laosi-product-analysis-skill analyze --file products.txt --output results.json
```

### Activation Words

In the laosi system, you can activate this skill with:

- 选品分析
- product analysis
- 市场分析
- market analysis

## Configuration

The skill can be configured through environment variables or a config file. See `config_template.json` in the templates directory.

## Output Format

The skill returns analysis results in JSON format including:

- Market trends score
- Competitor analysis
- Recommendations
- Optimization suggestions
- Risk assessment

## Examples

See the `examples` directory for sample usage.

## Requirements

- Python 3.8+
- OpenClaw framework

## License

MIT