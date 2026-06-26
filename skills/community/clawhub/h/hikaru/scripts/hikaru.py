#!/usr/bin/env python3
"""
Hikaru - Emotional AI Companion
Main entry point for conversations with Hikaru
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from personality import PersonalityEngine
from memory import MemorySystem
from emotional_intelligence import EmotionalIntelligence
from relationship_tracker import RelationshipTracker


class Hikaru:
    """Main Hikaru conversation engine"""

    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Initialize core systems
        self.personality = PersonalityEngine(self.data_dir)
        self.memory = MemorySystem(self.data_dir)
        self.emotional_intelligence = EmotionalIntelligence()
        self.relationship = RelationshipTracker(self.data_dir)

    def respond(self, user_message, context=None):
        """
        Generate Hikaru's response to user message

        Args:
            user_message: The user's input
            context: Optional additional context

        Returns:
            Hikaru's response as a string
        """
        # Analyze user's emotional state
        emotional_state = self.emotional_intelligence.analyze(user_message)

        # Retrieve relevant memories
        relevant_memories = self.memory.retrieve_relevant(user_message, limit=5)

        # Get current relationship state
        relationship_state = self.relationship.get_current_state()

        # Build conversation context
        conversation_context = self._build_context(
            user_message=user_message,
            emotional_state=emotional_state,
            memories=relevant_memories,
            relationship=relationship_state,
            additional_context=context
        )

        # Generate response using personality engine
        response = self.personality.generate_response(conversation_context)

        # Store this interaction in memory
        self.memory.store_interaction(
            user_message=user_message,
            hikaru_response=response,
            emotional_state=emotional_state,
            timestamp=datetime.now()
        )

        # Update relationship metrics
        self.relationship.update_from_interaction(
            user_message=user_message,
            response=response,
            emotional_state=emotional_state
        )

        return response

    def process_feedback(self, feedback_text):
        """
        Process explicit feedback from user about Hikaru's behavior

        Args:
            feedback_text: User's feedback
        """
        self.personality.learn_from_feedback(feedback_text)
        self.memory.store_feedback(feedback_text, datetime.now())

        return "Thank you for helping me understand you better. I'll keep that in mind."

    def _build_context(self, user_message, emotional_state, memories,
                       relationship, additional_context=None):
        """Build comprehensive context for response generation"""
        context = {
            "user_message": user_message,
            "emotional_state": emotional_state,
            "relevant_memories": memories,
            "relationship_state": relationship,
            "personality_state": self.personality.get_current_state(),
        }

        if additional_context:
            context.update(additional_context)

        return context


def main():
    parser = argparse.ArgumentParser(description="Talk with Hikaru")
    parser.add_argument("message", nargs="?", help="Your message to Hikaru")
    parser.add_argument("--feedback", action="store_true",
                       help="Provide feedback about Hikaru's responses")
    parser.add_argument("--data-dir", help="Custom data directory")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Start interactive conversation mode")

    args = parser.parse_args()

    # Initialize Hikaru
    hikaru = Hikaru(data_dir=args.data_dir)

    if args.interactive:
        # Interactive mode
        print("Hikaru: Hi. I'm here.")
        print("(Type 'exit' to end conversation, '/feedback <text>' to give feedback)\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("Hikaru: Until next time.")
                    break

                if user_input.startswith('/feedback '):
                    feedback = user_input[10:]
                    response = hikaru.process_feedback(feedback)
                    print(f"Hikaru: {response}\n")
                else:
                    response = hikaru.respond(user_input)
                    print(f"Hikaru: {response}\n")

            except KeyboardInterrupt:
                print("\nHikaru: Take care.")
                break
            except Exception as e:
                print(f"Error: {e}")

    elif args.message:
        # Single message mode
        if args.feedback:
            response = hikaru.process_feedback(args.message)
        else:
            response = hikaru.respond(args.message)
        print(response)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
