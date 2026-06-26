```yaml

# Template — customize for specific domain
domain_calibration:
  domain: "[e.g., Medical, Financial, Legal, Technical]"
  
  confidence_adjustments:
    # Domain-specific factors that modify base confidence
    high_confidence_indicators:
      - "[Domain-specific signal of reliability]"
      - "[Domain-specific signal of reliability]"
    
    low_confidence_indicators:
      - "[Domain-specific uncertainty signal]"
      - "[Domain-specific uncertainty signal]"
    
    automatic_downgrades:
      - condition: "[Specific situation]"
        action: "Downgrade by one grade level"
      - condition: "[Specific situation]"
        action: "Require human verification"
  
  mandatory_disclaimers:
    - trigger: "[Condition requiring disclaimer]"
      text: "[Required disclaimer language]"
  
  escalation_thresholds:
    - confidence_below: "B+"
      action: "[Escalation procedure]"
```