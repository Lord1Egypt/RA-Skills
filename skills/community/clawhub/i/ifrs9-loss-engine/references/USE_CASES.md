# Known Use Cases (KUC)

Total: **42**

## `KUC-101`
**Source**: `ECL/ECLLimitLevel_Truncate.ipynb`

Calculates Expected Credit Loss (ECL) at the limit/tranche level by computing remaining tenor and projecting loan balances with interest, supporting IFRS 9 impairment calculations.

## `KUC-102`
**Source**: `ECL/abAmortization.ipynb`

Computes loan amortization schedules by iteratively calculating interest amounts and remaining balances after each payment, determining total repayment terms.

## `KUC-103`
**Source**: `ECL/amortization.ipynb`

Generates amortization schedules using numpy-financial library functions (PMT, PPMT, IPMT) for calculating periodic payments, principal, and interest breakdown.

## `KUC-104`
**Source**: `LGD/LGDFunctionModel.ipynb`

Develops Loss Given Default (LGD) models using statistical regression techniques with 12-month forward observation windows for non-default populations.

## `KUC-105`
**Source**: `PD/APIBOTMacro.ipynb`

Fetches macroeconomic variables from Bank of Thailand's API including GDP, employment, and trade indicators for integration into credit risk models.

## `KUC-106`
**Source**: `PD/BOTNPLData.ipynb`

Cleans and processes raw NPL (Non-Performing Loan) data from Bank of Thailand, handling inconsistent column structures and formatting for credit risk analysis.

## `KUC-107`
**Source**: `PD/BayesCalibration.ipynb`

Calibrates credit rating transition matrices using Bayesian optimization methods to ensure row stochasticity and alignment with observed migration patterns.

## `KUC-108`
**Source**: `PD/CHAIDSegmentation.ipynb`

Segments used car loan customers using CHAID (Chi-squared Automatic Interaction Detection) decision tree algorithm with optimal binning for credit scoring development.

## `KUC-109`
**Source**: `PD/CooksDStudent.ipynb`

Identifies influential outliers and high-leverage points in PD regression models using Cook's distance and studentized residuals analysis.

## `KUC-110`
**Source**: `PD/HACAdjustment.ipynb`

Adjusts PD regression models for heteroscedasticity and autocorrelation using HAC (Heteroscedasticity and Autocorrelation Consistent) standard errors.

## `KUC-111`
**Source**: `PD/KMVModel.ipynb`

Implements the KMV-Merton structural model to estimate default probabilities from equity prices and market capitalization using option pricing theory.

## `KUC-112`
**Source**: `PD/LassoSelection.ipynb`

Selects optimal macroeconomic variables for PD models using LASSO (Least Absolute Shrinkage and Selection Operator) regression with time series cross-validation.

## `KUC-113`
**Source**: `PD/NRTMatrix.ipynb`

Constructs credit rating transition matrices for non-retail portfolios by counting rating migrations and computing conditional transition probabilities.

## `KUC-114`
**Source**: `PD/NelsonSiegelCurve.ipynb`

Fits Nelson-Siegel-Svensson curves to PD term structures for modeling the relationship between probability of default and time to maturity.

## `KUC-115`
**Source**: `PD/PDAssumedLGD.ipynb`

Defines assumed PD and LGD risk weights by asset class (Strong, Good, Satisfactory, Weak, Default) for regulatory capital and expected loss calculations.

## `KUC-116`
**Source**: `PD/PDCalibration.ipynb`

Calibrates Probability of Default from Through-the-Cycle (TTC) to Point-in-Time (PIT) estimates using central tendency adjustments and risk grade mapping.

## `KUC-117`
**Source**: `PD/PROCVARCLUS.ipynb`

Performs hierarchical variable clustering using VarClusHi algorithm to reduce multicollinearity among macroeconomic variables in PD models.

## `KUC-118`
**Source**: `PD/SilhouetteAnalysis.ipynb`

Evaluates optimal number of clusters in K-means segmentation using silhouette score analysis to determine best customer groupings for PD modeling.

## `KUC-119`
**Source**: `PD/TheoreticalMigrationMatrix.ipynb`

Constructs theoretically grounded migration matrices using parametric distributions and optimization to ensure mathematical consistency and economic plausibility.

## `KUC-120`
**Source**: `PD/allCombinations.ipynb`

Generates each possible combinations of macroeconomic variables within clusters for exhaustive model selection in PD development.

## `KUC-121`
**Source**: `PD/autoCorrTest.ipynb`

Tests for autocorrelation in PD model residuals using ACF plots, Ljung-Box test, and Durbin-Watson statistics to validate time series assumptions.

## `KUC-122`
**Source**: `PD/cci.ipynb`

Calculates Credit Conversion Index (CCI) by measuring downgrade rates and converting to a normalized z-score for stress testing and early warning systems.

## `KUC-123`
**Source**: `PD/chainLadder.ipynb`

Applies actuarial chain ladder methodology to estimate PD curves over time and aging buckets using weighted average calculations.

## `KUC-124`
**Source**: `PD/clusterSelection.ipynb`

Selects representative variables from clusters based on lowest R-square ratio and highest correlation for parsimonious PD model specification.

## `KUC-125`
**Source**: `PD/distributionSelection.ipynb`

Fits and compares multiple statistical distributions (Gamma, Log-normal, Weibull, etc.) to empirical PD risk grade curves for model selection.

## `KUC-126`
**Source**: `PD/externalMatrix.ipynb`

Integrates external credit ratings (e.g., Moody's) and their transition matrices with internal rating systems for PD benchmarking and calibration.

## `KUC-127`
**Source**: `PD/gammaFitting.ipynb`

Fits Gamma cumulative distribution functions to PD risk grade curves using scipy optimization to model default probability term structure.

## `KUC-128`
**Source**: `PD/generatorMatrix.ipynb`

Constructs generator (infinitesimal) matrices for continuous-time credit migration models enabling computation of transition probabilities over arbitrary time horizons.

## `KUC-129`
**Source**: `PD/heteroTest.ipynb`

Tests for heteroscedasticity in PD regression models using White's test and Breusch-Pagan test to validate homoscedasticity assumptions.

## `KUC-130`
**Source**: `PD/lifetimeCalibration.ipynb`

Calibrates lifetime PD curves using through-the-cycle (TTC) reference data and tracks calibration stability over time for IFRS 9 lifetime ECL calculations.

## `KUC-131`
**Source**: `PD/limitPDCurves.ipynb`

Applies limiting constraints to PD curves ensuring monotonicity, non-exceedance of regulatory floors, and compliance with Basel/IFRS 9 requirements.

## `KUC-132`
**Source**: `PD/multicolTest.ipynb`

Tests for multicollinearity among macroeconomic variables using Variance Inflation Factor (VIF) and correlation matrices in PD regression models.

## `KUC-133`
**Source**: `PD/normalityTest.ipynb`

Tests normality of regression residuals using Shapiro-Wilk, Anderson-Darling tests, QQ plots, and histograms for PD model assumption validation.

## `KUC-134`
**Source**: `PD/simplifiedCCI.ipynb`

Computes simplified Credit Conversion Index using z-score normalization of downgrade probabilities for portfolio-level credit stress monitoring.

## `KUC-135`
**Source**: `PD/survivalAnalysis.ipynb`

Applies survival analysis techniques to estimate lifetime default probabilities using Kaplan-Meier curves and Cox proportional hazards for IFRS 9 staging.

## `KUC-136`
**Source**: `PD/timeSeriesKMeans.ipynb`

Clusters macroeconomic time series using Dynamic Time Warping (DTW) distance with K-means algorithm to identify similar economic patterns for PD modeling.

## `KUC-137`
**Source**: `PD/timeSeriesStationary.ipynb`

Analyzes stationarity of macroeconomic time series using ADF tests and seasonal decomposition for proper model specification in PD regression.

## `KUC-138`
**Source**: `PD/transitionMatrix.ipynb`

Constructs empirical credit rating transition matrices from transaction-level data by tracking 12-month forward aging status and computing migration probabilities.

## `KUC-139`
**Source**: `PD/univariateAnalysis1.ipynb`

Performs univariate regression analysis on individual macroeconomic variables to assess their predictive power for ODR (Observed Default Rate) before multivariate modeling.

## `KUC-140`
**Source**: `PD/vasicekBaselRho.ipynb`

Estimates Basel Rho parameter (asset correlation) in the Vasicek single-factor model for regulatory capital calculation and portfolio credit risk.

## `KUC-141`
**Source**: `PD/vasicekTransitionMatrix.ipynb`

Calibrates credit rating transition matrices using the Vasicek asymptotic single risk factor model ensuring consistency with Basel regulatory requirements.

## `KUC-142`
**Source**: `Staging/backwardTransaction.ipynb`

Processes backward-looking transaction data to create performance windows and default flags for credit scoring model development in staging environments.
