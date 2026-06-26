#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emotional Analyzer
情感分析模块 - Clawvard EQ改进
"""

import re
from typing import Dict, List, Tuple
from enum import Enum

class EmotionType(Enum):
    """情绪类型"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    ANGRY = "angry"
    HAPPY = "happy"
    SAD = "sad"
    SURPRISED = "surprised"
    FEARFUL = "fearful"

class EmotionalAnalyzer:
    """情感分析器"""
    
    def __init__(self):
        self.emotion_keywords = {
            EmotionType.POSITIVE: [
                'good', 'great', 'excellent', 'amazing', 'wonderful',
                'happy', 'love', 'like', 'enjoy', 'pleased',
                'thank', 'thanks', 'appreciate', 'grateful'
            ],
            EmotionType.NEGATIVE: [
                'bad', 'terrible', 'awful', 'horrible', 'poor',
                'hate', 'dislike', 'angry', 'frustrated', 'annoyed',
                'sad', 'disappointed', 'upset', 'worried'
            ],
            EmotionType.ANGRY: [
                'angry', 'furious', 'mad', 'rage', 'hate',
                'annoyed', 'frustrated', 'irritated', 'pissed'
            ],
            EmotionType.HAPPY: [
                'happy', 'joy', 'excited', 'thrilled', 'delighted',
                'cheerful', 'glad', 'pleased', 'satisfied'
            ],
            EmotionType.SAD: [
                'sad', 'depressed', 'unhappy', 'miserable', 'down',
                'disappointed', 'heartbroken', 'grief'
            ],
            EmotionType.SURPRISED: [
                'surprised', 'shocked', 'amazed', 'astonished',
                'unexpected', 'wow', 'incredible'
            ],
            EmotionType.FEARFUL: [
                'afraid', 'scared', 'fear', 'worried', 'anxious',
                'nervous', 'terrified', 'panic'
            ]
        }
        
        self.intensity_modifiers = {
            'very': 1.5,
            'extremely': 2.0,
            'really': 1.3,
            'quite': 1.2,
            'somewhat': 0.8,
            'a little': 0.6,
            'slightly': 0.7
        }
    
    def analyze(self, text: str) -> Dict:
        """
        分析文本情感
        
        Args:
            text: 输入文本
            
        Returns:
            情感分析结果
        """
        text_lower = text.lower()
        
        # 检测强度修饰词
        intensity = 1.0
        for modifier, factor in self.intensity_modifiers.items():
            if modifier in text_lower:
                intensity = factor
                break
        
        # 检测情绪
        emotion_scores = {}
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            emotion_scores[emotion] = score * intensity
        
        # 确定主要情绪
        if not emotion_scores or max(emotion_scores.values()) == 0:
            primary_emotion = EmotionType.NEUTRAL
            confidence = 0.5
        else:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = min(emotion_scores[primary_emotion] / 3.0, 1.0)
        
        return {
            'primary_emotion': primary_emotion.value,
            'confidence': confidence,
            'intensity': intensity,
            'all_scores': {e.value: s for e, s in emotion_scores.items()},
            'text': text
        }
    
    def detect_sentiment(self, text: str) -> Tuple[str, float]:
        """
        检测情感倾向（正面/负面/中性）
        
        Args:
            text: 输入文本
            
        Returns:
            (情感倾向, 置信度)
        """
        result = self.analyze(text)
        
        if result['primary_emotion'] in ['positive', 'happy']:
            return 'positive', result['confidence']
        elif result['primary_emotion'] in ['negative', 'angry', 'sad', 'fearful']:
            return 'negative', result['confidence']
        else:
            return 'neutral', result['confidence']
    
    def get_emotional_response(self, text: str) -> str:
        """
        生成情感响应
        
        Args:
            text: 输入文本
            
        Returns:
            响应文本
        """
        sentiment, confidence = self.detect_sentiment(text)
        
        if sentiment == 'positive' and confidence > 0.6:
            return "I'm glad to hear that! Is there anything else I can help you with?"
        elif sentiment == 'negative' and confidence > 0.6:
            return "I understand you're frustrated. Let me help you resolve this issue."
        else:
            return "I see. How can I assist you further?"
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """
        批量分析文本情感
        
        Args:
            texts: 文本列表
            
        Returns:
            情感分析结果列表
        """
        return [self.analyze(text) for text in texts]


if __name__ == "__main__":
    analyzer = EmotionalAnalyzer()
    
    # 测试
    test_texts = [
        "I'm very happy with this!",
        "This is terrible and I hate it.",
        "I'm somewhat disappointed.",
        "This is just okay."
    ]
    
    for text in test_texts:
        result = analyzer.analyze(text)
        print(f"Text: {text}")
        print(f"Emotion: {result['primary_emotion']} (confidence: {result['confidence']:.2f})")
        print(f"Response: {analyzer.get_emotional_response(text)}")
        print()
