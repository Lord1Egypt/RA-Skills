"""Registry package for model metadata, pricing, and aliases."""

from .models import (  # noqa: F401
    ModelInfo,
    get_all_supported_models,
    get_model_info,
    get_supported_models_by_provider,
    normalize_model_name,
)
from .pricing import USD_TO_INR, get_pricing_rate  # noqa: F401
