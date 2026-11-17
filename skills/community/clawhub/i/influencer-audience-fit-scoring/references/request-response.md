# Request and Response Guide

## `GET /api/v1/audience/instagram/age`
- operationId: `audience_instagram_age`
- summary: 年龄(age)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "13-17": "20.04%",
    "18-24": "29.06%",
    "25-34": "24.27%",
    "35-44": "10.16%",
    "45-54": "8.28%",
    "55-64": "4.62%",
    "65+": "3.57%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/instagram/brand_opportunities`
- operationId: `audience_instagram_brand_opportunities`
- summary: 营销路径(brand opportunities)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_AudienceBrandOpportunitiesItem_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `audience_quality`, `purchase_influence`, `personality_assessment`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "audience_quality": {
      "real": {
        "score": "80.00",
        "reason": "Analysis shows that approximately 80% of comments are relevant and contextually engaged with Nike's content."
      },
      "interested": {
        "score": "65.00",
        "reason": "65% of comments express interest in products or features, indicating a solid level of purchase intent."
      },
      "positive": {
        "score": "70.00",
        "reason": "70% positive sentiment in comments suggests overall appreciation for Nike's branding efforts despite recent controversies."
      }
    },
    "purchase_influence": {
      "expertise": {
        "score": "4.00",
        "reason": "'Breaking4' campaign effectively showcases product benefits through high-profile athlete endorsements, enhancing purchase intent."
      },
      "credibility": {
        "score": "3.50",
        "reason": "'Nike's transparency in partnerships is commendable, but recent controversies have led to some skepticism among followers.'"
      },
      "likability": {
        "score": "3.80",
        "reason": "'High engagement rates indicate positive community interaction; however, negative comments reflect divided opinions on brand actions.'"
      }
    },
    "personality_assessment": [
      {
        "emoji": "💪",
        "name": "Resilience",
        "persona": "Demonstrates strong perseverance and determination, inspiring followers to push their limits in sports and fitness."
      }
    ]
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/instagram/content_style`
- operationId: `audience_instagram_content_style`
- summary: 社交人格(content style)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_AudienceContentStyleItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.name`, `items.desc`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "name": "Announcer",
      "desc": "Nike fits the Announcer personality type because they broadcast great content that spreads widely, especially around major events like Breaking4. Their broad, diverse audience values their content, and they serve as an important source of information in the sports and fitness industry."
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/instagram/device`
- operationId: `audience_instagram_device`
- summary: 设备占比(device)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_AudienceDevicePercentageItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.name`, `items.value`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "name": "ios",
      "value": "0.4365"
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/instagram/follower_authenticity`
- operationId: `audience_instagram_follower_authenticity`
- summary: 粉丝真实性(follower authenticity)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_AudienceFollowerAuthenticityRep_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `real`, `fake`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "real": "90%",
    "fake": "10%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/instagram/gender`
- operationId: `audience_instagram_gender`
- summary: 性别(gender)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__Dict_str__str___` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "13-17": {
      "female": "55.45%",
      "male": "44.55%"
    },
    "18-24": {
      "female": "50.76%",
      "male": "49.24%"
    },
    "25-34": {
      "female": "45.90%",
      "male": "54.10%"
    },
    "35-44": {
      "female": "40.48%",
      "male": "59.52%"
    },
    "45-54": {
      "female": "35.73%",
      "male": "64.27%"
    },
    "55-64": {
      "female": "30.97%",
      "male": "69.03%"
    },
    "65+": {
      "female": "25.46%",
      "male": "74.54%"
    }
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/instagram/gender_overall`
- operationId: `audience_instagram_gender_overall`
- summary: 整体性别(gender overall)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "female": "50.00%",
    "male": "50.00%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/instagram/geography`
- operationId: `audience_instagram_geography`
- summary: 地理位置(geography)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "US": "43.99%",
    "IN": "15.07%",
    "GB": "9.76%",
    "CA": "8.63%",
    "AU": "5.18%",
    "DE": "4.41%",
    "FR": "3.79%",
    "MX": "3.66%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/instagram/interactive_behavior`
- operationId: `audience_instagram_interactive_behavior`
- summary: 互动行为(interactive behavior)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_AudienceInteractiveBehaviorItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.role`, `items.value`, `items.demographic`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "role": "Viewer",
      "value": "60.00",
      "demographic": "Primarily young adults and teenagers who enjoy entertaining content."
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/instagram/interest`
- operationId: `audience_instagram_interest`
- summary: 兴趣(interest)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_AudienceInterestItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.interest`, `items.value`, `items.illustration`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "interest": "Philanthropy",
      "value": "30.00",
      "illustration": "The audience is drawn to MrBeast's charitable acts, such as planting trees and helping those in need."
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/instagram/language`
- operationId: `audience_instagram_language`
- summary: 语言(language)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "en": "71.01%",
    "hi": "10.86%",
    "es": "8.94%",
    "pt": "5.17%",
    "de": "4.02%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/instagram/rating_tier`
- operationId: `audience_instagram_rating_tier`
- summary: 评级等级(rating tier)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `username` | `query` | `true` | `string` | username |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_AudienceRatingTierRep_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `rating_tier`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "rating_tier": "HIGH"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/age`
- operationId: `audience_tiktok_age`
- summary: 年龄(age)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "13-17": "20.04%",
    "18-24": "29.06%",
    "25-34": "24.27%",
    "35-44": "10.16%",
    "45-54": "8.28%",
    "55-64": "4.62%",
    "65+": "3.57%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/brand_opportunities`
- operationId: `audience_tiktok_brand_opportunities`
- summary: 营销路径(brand opportunities)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_AudienceBrandOpportunitiesItem_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `audience_quality`, `purchase_influence`, `personality_assessment`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "audience_quality": {
      "real": {
        "score": "68.50",
        "reason": "Mixed authenticity with notable spam but also genuine fan interactions."
      },
      "interested": {
        "score": "52.00",
        "reason": "Moderate product interest with some detailed inquiries amid generic reactions."
      },
      "positive": {
        "score": "82.70",
        "reason": "Predominantly upbeat sentiment though diluted by repetitive/spammy comments."
      }
    },
    "purchase_influence": {
      "expertise": {
        "score": "4.30",
        "reason": "High-quality product showcases with detailed features but lacks consistent demonstration depth."
      },
      "credibility": {
        "score": "4.00",
        "reason": "Strong brand trust but occasional skepticism over sponsorship transparency in comments."
      },
      "likability": {
        "score": "4.50",
        "reason": "Exceptional audience rapport with frequent positive interactions and community-building efforts."
      }
    },
    "personality_assessment": [
      {
        "emoji": "🏆",
        "name": "Inspirational",
        "persona": "Consistently motivates and uplifts followers with high-energy content and positive messaging."
      }
    ]
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/content_style`
- operationId: `audience_tiktok_content_style`
- summary: 社交人格(content style)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_AudienceContentStyleItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.name`, `items.desc`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "name": "Announcer",
      "desc": "Nike fits the Announcer personality type because they broadcast great content that spreads widely, especially around major events like Breaking4. Their broad, diverse audience values their content, and they serve as an important source of information in the sports and fitness industry."
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/device`
- operationId: `audience_tiktok_device`
- summary: 设备占比(device)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_AudienceDevicePercentageItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.name`, `items.value`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "name": "ios",
      "value": "0.4365"
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/follower_authenticity`
- operationId: `audience_tiktok_follower_authenticity`
- summary: 粉丝真实性(follower authenticity)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_AudienceFollowerAuthenticityRep_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `real`, `fake`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "real": "90%",
    "fake": "10%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/gender`
- operationId: `audience_tiktok_gender`
- summary: 性别(gender)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__Dict_str__str___` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "13-17": {
      "female": "55.45%",
      "male": "44.55%"
    },
    "18-24": {
      "female": "50.76%",
      "male": "49.24%"
    },
    "25-34": {
      "female": "45.90%",
      "male": "54.10%"
    },
    "35-44": {
      "female": "40.48%",
      "male": "59.52%"
    },
    "45-54": {
      "female": "35.73%",
      "male": "64.27%"
    },
    "55-64": {
      "female": "30.97%",
      "male": "69.03%"
    },
    "65+": {
      "female": "25.46%",
      "male": "74.54%"
    }
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/gender_overall`
- operationId: `audience_tiktok_gender_overall`
- summary: 整体性别(gender overall)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "female": "50.00%",
    "male": "50.00%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/geography`
- operationId: `audience_tiktok_geography`
- summary: 地理位置(geography)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "US": "43.99%",
    "IN": "15.07%",
    "GB": "9.76%",
    "CA": "8.63%",
    "AU": "5.18%",
    "DE": "4.41%",
    "FR": "3.79%",
    "MX": "3.66%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/interactive_behavior`
- operationId: `audience_tiktok_interactive_behavior`
- summary: 互动行为(interactive behavior)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_AudienceInteractiveBehaviorItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.role`, `items.value`, `items.demographic`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "role": "Viewer",
      "value": "60.00",
      "demographic": "Primarily young adults and teenagers who enjoy entertaining content."
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/interest`
- operationId: `audience_tiktok_interest`
- summary: 兴趣(interest)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_AudienceInterestItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.interest`, `items.value`, `items.illustration`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "interest": "Philanthropy",
      "value": "30.00",
      "illustration": "The audience is drawn to MrBeast's charitable acts, such as planting trees and helping those in need."
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/language`
- operationId: `audience_tiktok_language`
- summary: 语言(language)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "en": "71.01%",
    "hi": "10.86%",
    "es": "8.94%",
    "pt": "5.17%",
    "de": "4.02%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/tiktok/rating_tier`
- operationId: `audience_tiktok_rating_tier`
- summary: 评级等级(rating tier)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `unique_id` | `query` | `true` | `string` | unique_id |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_AudienceRatingTierRep_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `rating_tier`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "rating_tier": "HIGH"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/youtube/age`
- operationId: `audience_youtube_age`
- summary: 年龄(age)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "13-17": "20.04%",
    "18-24": "29.06%",
    "25-34": "24.27%",
    "35-44": "10.16%",
    "45-54": "8.28%",
    "55-64": "4.62%",
    "65+": "3.57%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/youtube/brand_opportunities`
- operationId: `audience_youtube_brand_opportunities`
- summary: 营销路径(brand opportunities)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_AudienceBrandOpportunitiesItem_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `audience_quality`, `purchase_influence`, `personality_assessment`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "audience_quality": {
      "real": {
        "score": "90.00",
        "reason": "Analysis shows high engagement rates with meaningful comments indicating authentic follower interaction across multiple videos."
      },
      "interested": {
        "score": "75.00",
        "reason": "75% of comments discuss specific video features or express interest in related products, indicating strong purchase intent."
      },
      "positive": {
        "score": "85.00",
        "reason": "Majority of comments reflect admiration for MrBeast's generosity and creativity, contributing to an overwhelmingly positive sentiment."
      }
    },
    "purchase_influence": {
      "expertise": {
        "score": "4.70",
        "reason": "'Buy Feastables! It tastes amazing' effectively promotes products with engaging visuals and personal endorsements throughout videos."
      },
      "credibility": {
        "score": "4.50",
        "reason": "High trust established through transparency about sponsorships, though some comments express skepticism about product authenticity."
      },
      "likability": {
        "score": "4.80",
        "reason": "Strong positive engagement with followers through humor and relatability fosters a loyal community eager to support."
      }
    },
    "personality_assessment": [
      {
        "emoji": "🌟",
        "name": "Generosity",
        "persona": "Consistently engages in philanthropic activities, positively impacting communities and inspiring followers to contribute."
      }
    ]
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/youtube/content_style`
- operationId: `audience_youtube_content_style`
- summary: 社交人格(content style)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_AudienceContentStyleItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.name`, `items.desc`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "name": "Celebrity",
      "desc": "MrBeast is at the pinnacle of influence with a massive subscriber count and high engagement rates. His content spreads widely, and his audience is highly engaged, showing characteristics of a celebrity influencer. His followers are deeply invested in his content, and his influence extends globally."
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/youtube/follower_authenticity`
- operationId: `audience_youtube_follower_authenticity`
- summary: 粉丝真实性(follower authenticity)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_AudienceFollowerAuthenticityRep_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `real`, `fake`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "real": "90%",
    "fake": "10%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/youtube/gender`
- operationId: `audience_youtube_gender`
- summary: 性别(gender)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__Dict_str__str___` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "13-17": {
      "female": "55.45%",
      "male": "44.55%"
    },
    "18-24": {
      "female": "50.76%",
      "male": "49.24%"
    },
    "25-34": {
      "female": "45.90%",
      "male": "54.10%"
    },
    "35-44": {
      "female": "40.48%",
      "male": "59.52%"
    },
    "45-54": {
      "female": "35.73%",
      "male": "64.27%"
    },
    "55-64": {
      "female": "30.97%",
      "male": "69.03%"
    },
    "65+": {
      "female": "25.46%",
      "male": "74.54%"
    }
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/youtube/gender_overall`
- operationId: `audience_youtube_gender_overall`
- summary: 整体性别(gender overall)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "female": "50.00%",
    "male": "50.00%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/youtube/geography`
- operationId: `audience_youtube_geography`
- summary: 地理位置(geography)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "US": "43.99%",
    "IN": "15.07%",
    "GB": "9.76%",
    "CA": "8.63%",
    "AU": "5.18%",
    "DE": "4.41%",
    "FR": "3.79%",
    "MX": "3.66%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/youtube/interactive_behavior`
- operationId: `audience_youtube_interactive_behavior`
- summary: 互动行为(interactive behavior)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_AudienceInteractiveBehaviorItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.role`, `items.value`, `items.demographic`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "role": "Viewer",
      "value": "60.00",
      "demographic": "Primarily young adults and teenagers who enjoy entertaining content."
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/youtube/interest`
- operationId: `audience_youtube_interest`
- summary: 兴趣(interest)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
| `X-Language` | `header` | `false` | `string` | 语言代码,支持: ['en', 'zh-CN', 'ja', 'ko'] |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_list_AudienceInterestItem__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `items.interest`, `items.value`, `items.illustration`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": [
    {
      "interest": "Philanthropy",
      "value": "30.00",
      "illustration": "The audience is drawn to MrBeast's charitable acts, such as planting trees and helping those in need."
    }
  ]
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/youtube/language`
- operationId: `audience_youtube_language`
- summary: 语言(language)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_Dict_str__str__` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `<dynamic object keys>`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "en": "71.01%",
    "hi": "10.86%",
    "es": "8.94%",
    "pt": "5.17%",
    "de": "4.02%"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## `GET /api/v1/audience/youtube/rating_tier`
- operationId: `audience_youtube_rating_tier`
- summary: 评级等级(rating tier)
- parameters:
| name | in | required | schema | description |
|---|---|---|---|---|
| `channel_id` | `query` | `true` | `string` | 频道ID |
- requestBody: none
- responses:
| status | content-type | schema |
|---|---|---|
| `200` | `application/json` | `ResponseModel_AudienceRatingTierRep_` |
| `422` | `application/json` | `HTTPValidationError` |
- `200` top-level fields: `success`, `code`, `message`, `data`
- `200` data level-1 fields: `rating_tier`
- `200` minimal example:
```json
{
  "success": true,
  "code": 200,
  "message": "请求成功",
  "data": {
    "rating_tier": "HIGH"
  }
}
```
- `422` top-level fields: `detail`
- `422` data level-1 fields: none
- `422` minimal example:
```json
{
  "detail": [
    {
      "loc": [
        null
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```
