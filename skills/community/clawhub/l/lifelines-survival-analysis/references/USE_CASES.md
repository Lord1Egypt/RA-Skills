# Known Use Cases (KUC)

Total: **19**

## `KUC-101`
**Source**: `examples/Cox residuals.ipynb`

Diagnosing Cox proportional hazards model fit by computing and visualizing martingale, deviance, and delta_beta residuals to identify outliers and influential observations.

## `KUC-102`
**Source**: `examples/Custom Regression Models.ipynb`

Creating user-defined parametric survival regression models by subclassing ParametricRegressionFitter to implement custom hazard functions for specialized applications.

## `KUC-103`
**Source**: `examples/Modelling time-lagged conversion rates.ipynb`

Modeling marketing conversion rates where there is a time lag between initial contact and conversion event, requiring specialized survival analysis techniques.

## `KUC-104`
**Source**: `examples/Piecewise Exponential Models and Creating Custom Models.ipynb`

Fitting piecewise exponential survival models that allow different hazard rates in different time intervals, useful when hazard is non-constant over time.

## `KUC-105`
**Source**: `examples/Proportional hazard assumption.ipynb`

Validating that the proportional hazards assumption holds for Cox models using statistical tests and visual diagnostics, and applying remedies like stratification or splines when violations occur.

## `KUC-106`
**Source**: `examples/B-splines.ipynb`

Using B-splines in Cox proportional hazards models to flexibly model non-linear relationships between covariates and hazard without assuming specific functional forms.

## `KUC-107`
**Source**: `examples/SaaS churn and piecewise regression models.ipynb`

Predicting customer churn in SaaS subscription business using survival analysis, accounting for varying churn rates across customer tenure segments.

## `KUC-108`
**Source**: `examples/US Presidential Cabinet survival.ipynb`

Analyzing tenure survival of US presidential cabinet members across administrations, examining factors affecting cabinet turnover and duration.

## `KUC-109`
**Source**: `examples/aalen_and_cook_simulation.py`

Simulation study for Aalen-Johansen estimator and comparison with Cox/Weibull models to understand multi-state survival dynamics.

## `KUC-110`
**Source**: `examples/copula_frailty_weibull_model.py`

Modeling dependent competing risks using copula-based frailty to account for unobserved heterogeneity that creates correlation between multiple failure types.

## `KUC-111`
**Source**: `examples/cox_spline_custom_knots.py`

Fitting Cox proportional hazards model with spline-based baseline hazard using user-specified knot locations for flexible survival modeling.

## `KUC-112`
**Source**: `examples/crowther_royston_clements_splines.py`

Implementing flexible parametric accelerated failure time models using Royston-Clements splines for flexible baseline survival estimation.

## `KUC-113`
**Source**: `examples/cure_model.py`

Modeling survival data where a proportion of subjects will never experience the event (cured), using Weibull survival with cure component.

## `KUC-114`
**Source**: `examples/haft_model.py`

Implementing heteroscedastic accelerated failure time models where variance of log-survival time depends on covariates, providing more flexible survival modeling.

## `KUC-115`
**Source**: `examples/left_censoring_experiments.py`

Handling left-censored survival data where the true event time may have occurred before the observation window began, common in environmental or detection-limited data.

## `KUC-116`
**Source**: `examples/mixture_cure_model.py`

Modeling survival with multiple cure pathways using mixture models to represent different subgroups with different probabilities of experiencing the event.

## `KUC-117`
**Source**: `examples/Solving a mixture of exponentials and binning using interval censoring.ipynb`

Fitting mixture of exponential distributions to interval-censored data, where exact event times are unknown but fall within observed intervals.

## `KUC-118`
**Source**: `experiments/Experiments on primary and secondary shelf life.ipynb`

Analyzing product shelf life using competing risks framework to model both primary shelf life (time to first event) and secondary shelf life (time between events).

## `KUC-119`
**Source**: `docs/images/dist_script.py`

Visualizing Weibull survival functions to understand how shape and scale parameters affect survival curves for educational and model selection purposes.
