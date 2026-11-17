# Machine Learning Reference

Baseline ML workflows with scikit-learn: classification, regression, clustering, feature engineering, model persistence. **Load this reference when the user wants to fit/predict/cluster on tabular data.**

## Setup

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score,
    mean_squared_error, r2_score, mean_absolute_error,
    silhouette_score, calinski_harabasz_score,
)
np.random.seed(42)  # reproducibility
```

## Classification Pipeline

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

# Split — stratify preserves class balance
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42,
)

# Pipeline — scaler + classifier
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)),
])

pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
print(classification_report(y_test, y_pred))

# ROC AUC (binary or one-vs-rest)
if len(np.unique(y)) == 2:
    y_proba = pipe.predict_proba(X_test)[:, 1]
    print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.3f}")
```

### Cross-validation (more reliable than single split)
```python
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipe, X, y, cv=cv, scoring='f1_weighted')
print(f"CV F1: {scores.mean():.3f} ± {scores.std() * 2:.3f}")
```

### Grid search
```python
param_grid = {
    'clf__n_estimators': [50, 100, 200],
    'clf__max_depth': [None, 10, 20],
    'clf__min_samples_leaf': [1, 5, 10],
}
grid = GridSearchCV(pipe, param_grid, cv=cv, scoring='f1_weighted', n_jobs=-1)
grid.fit(X_train, y_train)
print(f"Best params: {grid.best_params_}")
print(f"Best CV score: {grid.best_score_:.3f}")
print(f"Test score: {grid.score(X_test, y_test):.3f}")
```

## Regression Pipeline

```python
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('reg', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)),
])
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"R²:  {r2_score(y_test, y_pred):.3f}")
print(f"RMSE: {rmse:.3f}")
print(f"MAE:  {mean_absolute_error(y_test, y_pred):.3f}")
```

### Compare multiple models
```python
models = {
    'ridge': Pipeline([('scaler', StandardScaler()), ('reg', Ridge())]),
    'rf':    Pipeline([('scaler', StandardScaler()), ('reg', RandomForestRegressor(n_estimators=100, random_state=42))]),
    'gbm':   Pipeline([('scaler', StandardScaler()), ('reg', GradientBoostingRegressor(random_state=42))]),
}
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring='neg_root_mean_squared_error')
    print(f"{name:8s} RMSE: {-scores.mean():.3f} ± {scores.std() * 2:.3f}")
```

## Clustering

```python
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering

X_scaled = StandardScaler().fit_transform(X)

# Choose k via silhouette score
for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    print(f"k={k}: silhouette={score:.3f}, inertia={km.inertia_:.0f}")

# Fit final model
best_k = 4  # pick from above
km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
labels = km.fit_predict(X_scaled)

# DBSCAN for density-based clustering (no preset k)
db = DBSCAN(eps=0.5, min_samples=5)
labels_db = db.fit_predict(X_scaled)
n_clusters = len(set(labels_db)) - (1 if -1 in labels_db else 0)
n_noise = (labels_db == -1).sum()
print(f"DBSCAN: {n_clusters} clusters, {n_noise} noise points")
```

## Feature Engineering

```python
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.decomposition import PCA

# Select top-k by F-test
selector = SelectKBest(f_classif, k=10)
X_selected = selector.fit_transform(X, y)
selected_mask = selector.get_support()
print("Selected features:", [features[i] for i in range(len(features)) if selected_mask[i]])

# PCA for visualization or dimensionality reduction
pca = PCA(n_components=2)
X_pca = pca.fit_transform(StandardScaler().fit_transform(X))
print(f"Explained variance: {pca.explained_variance_ratio_.sum():.2%}")

# Recursive feature elimination (slow but accurate)
rfe = RFE(
    estimator=RandomForestClassifier(n_estimators=50, random_state=42),
    n_features_to_select=10,
)
rfe.fit(X, y)
print("RFE features:", [features[i] for i in range(len(features)) if rfe.support_[i]])
```

## Model Persistence

```python
import joblib

# Save (includes preprocessing pipeline + model)
joblib.dump(pipe, '/home/z/my-project/download/model.joblib', compress=3)

# Load
loaded = joblib.load('/home/z/my-project/download/model.joblib')
predictions = loaded.predict(new_data)
```

For sklearn models, `joblib` is preferred over `pickle` — it handles numpy arrays efficiently and supports compression.

## Common Pitfalls

### Data leakage
- Fit scaler on training data only, then transform test data: `scaler.fit(X_train); scaler.transform(X_test)`. Using a Pipeline handles this automatically.
- Don't use target-derived features (e.g., binning by quantile of `y`) before the split.
- Time-series: use `TimeSeriesSplit`, not random `KFold`.

### Imbalanced classes
```python
# Stratified split preserves balance
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2)

# Class-weighted model
clf = RandomForestClassifier(class_weight='balanced', n_estimators=100)

# Or SMOTE oversampling (imbalanced-learn)
# from imblearn.over_sampling import SMOTE
# X_res, y_res = SMOTE(random_state=42).fit_resample(X_train, y_train)
```

### Categorical encoding
```python
# Ordinal (low-cardinality, ordered)
df['grade_encoded'] = df['grade'].map({'A': 0, 'B': 1, 'C': 2})

# One-hot (low-cardinality, unordered)
df = pd.get_dummies(df, columns=['color'], prefix='color')

# Target encoding (high-cardinality) — use category_encoders library
# from category_encoders import TargetEncoder
# enc = TargetEncoder(cols=['zip_code'])
# df['zip_encoded'] = enc.fit_transform(df['zip_code'], df['target'])
```

## Workflow: First ML Pass on New Data

1. **EDA** (use `references/data-analysis.md`): understand distributions, missing values, target balance.
2. **Baseline**: fit a simple model (LogisticRegression for classification, Ridge for regression) with cross-validation. This is the floor — anything more complex must beat it.
3. **Feature engineering**: try the most promising 2-3 features, not all of them.
4. **Model selection**: compare 3-4 models with `cross_val_score`. Don't grid-search yet.
5. **Hyperparameter tuning**: grid-search only the best 1-2 models.
6. **Final evaluation**: report on held-out test set. Save model with `joblib.dump`.
