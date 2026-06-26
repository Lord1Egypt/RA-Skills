# Known Use Cases (KUC)

Total: **6**

## `KUC-101`
**Source**: `cookbook/1-RiskReturnModels.ipynb`

Compares multiple covariance estimation methods (sample, semicovariance, exponential, Ledoit-Wolf variants, oracle approximating) to evaluate which provides the most accurate risk estimates for portfolio construction.

## `KUC-102`
**Source**: `cookbook/2-Mean-Variance-Optimisation.ipynb`

Constructs a minimum volatility portfolio using mean-variance optimization with CAPM-based expected returns and compares sample covariance vs Ledoit-Wolf shrinkage estimators.

## `KUC-103`
**Source**: `cookbook/3-Advanced-Mean-Variance-Optimisation.ipynb`

Implements advanced mean-variance optimization that accounts for broker transaction costs when rebalancing from an initial portfolio allocation, using semicovariance as the risk model.

## `KUC-104`
**Source**: `cookbook/4-Black-Litterman-Allocation.ipynb`

Combines market equilibrium prior returns with investor views using the Black-Litterman model to generate more realistic expected returns and construct portfolios that reflect both market consensus and proprietary opinions.

## `KUC-105`
**Source**: `cookbook/5-Hierarchical-Risk-Parity.ipynb`

Constructs a diversified portfolio using Hierarchical Risk Parity (HRP), which uses clustering/dendrogram analysis to group correlated assets and allocate weights without requiring covariance matrix inversion.

## `KUC-106`
**Source**: `docs/conf.py`

Sphinx documentation configuration file for building PyPortfolioOpt package documentation, not a functional portfolio strategy.
