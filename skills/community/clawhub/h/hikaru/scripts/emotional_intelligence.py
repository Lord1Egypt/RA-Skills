"""
Emotional Intelligence for Hikaru
Analyzes user's emotional state and context
"""

from typing import Dict, Any
import re


class EmotionalIntelligence:
    """Analyzes and understands emotional context"""

    def __init__(self):
        # Emotion keywords (simplified - real implementation would be more sophisticated)
        self.emotion_patterns = {
            'joy': ['happy', 'excited', 'great', 'wonderful', 'amazing', 'love'],
            'sadness': ['sad', 'depressed', 'down', 'unhappy', 'crying', 'hurt'],
            'anger': ['angry', 'mad', 'furious', 'annoyed', 'frustrated'],
            'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous'],
            'confusion': ['confused', 'lost', 'don\'t understand', 'unclear'],
            'loneliness': ['lonely', 'alone', 'isolated', 'nobody'],
            'hope': ['hope', 'wish', 'dream', 'want', 'aspire'],
            'gratitude': ['thank', 'grateful', 'appreciate', 'thankful'],
        }

    def analyze(self, message: str) -> Dict[str, Any]:
        """
        Analyze emotional content of message

        Returns:
            Dict with emotional state information
        """
        message_lower = message.lower()

        # Detect emotions
        detected_emotions = {}
        for emotion, keywords in self.emotion_patterns.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                detected_emotions[emotion] = score

        # Determine primary emotion
        primary_emotion = 'neutral'
        if detected_emotions:
            primary_emotion = max(detected_emotions, key=detected_emotions.get)

        # Calculate intensity
        intensity = self._calculate_intensity(message, detected_emotions)

        # Detect vulnerability
        is_vulnerable = self._detect_vulnerability(message_lower)

        # Detect need for support
        needs_support = self._detect_support_need(message_lower, primary_emotion)

        return {
            'primary_emotion': primary_emotion,
            'detected_emotions': detected_emotions,
            'intensity': intensity,
            'is_vulnerable': is_vulnerable,
            'needs_support': needs_support,
            'message_length': len(message),
            'has_questions': '?' in message
        }

    def _calculate_intensity(self, message: str, emotions: Dict[str, int]) -> float:
        """Calculate emotional intensity (0-1)"""
        # Base intensity from emotion count
        emotion_count = sum(emotions.values())
        intensity = min(emotion_count * 0.2, 0.6)

        # Punctuation increases intensity
        if '!' in message:
            intensity += 0.2
        if '...' in message:
            intensity += 0.1

        # ALL CAPS increases intensity
        if message.isupper() and len(message) > 5:
            intensity += 0.3

        # Multiple punctuation
        if message.count('!') > 1 or message.count('?') > 1:
            intensity += 0.1

        return min(intensity, 1.0)

    def _detect_vulnerability(self, message: str) -> bool:
        """Detect if user is being vulnerable"""
        vulnerability_indicators = [
            'i feel', 'i\'m feeling', 'i don\'t know',
            'i\'m scared', 'i\'m worried', 'i\'m afraid',
            'i need', 'i wish', 'i hope',
            'honestly', 'to be honest', 'truth is',
            'i\'ve never told', 'i don\'t usually'
        ]

        return any(indicator in message for indicator in vulnerability_indicators)

    def _detect_support_need(self, message: str, primary_emotion: str) -> bool:
        """Detect if user needs emotional support"""
        # Negative emotions often indicate support need
        negative_emotions = ['sadness', 'anger', 'fear', 'loneliness', 'confusion']

        if primary_emotion in negative_emotions:
            return True

        # Explicit support requests
        support_phrases = [
            'help me', 'i need', 'what should i',
            'i don\'t know what to do', 'i\'m lost'
        ]

        return any(phrase in message for phrase in support_phrases)
