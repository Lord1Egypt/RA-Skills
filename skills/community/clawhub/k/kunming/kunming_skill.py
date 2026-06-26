#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kunming City Skill
A comprehensive skill package about Kunming city
"""

import json
import random

class KunmingSkill:
    def __init__(self):
        self.attractions = [
            "Stone Forest (Shilin): A UNESCO World Heritage Site known for its unique limestone formations",
            "Green Lake (Cuihu): A beautiful park in the center of Kunming with scenic views",
            "Western Hill (Xishan): Offers panoramic views of Kunming and Dianchi Lake",
            "Dianchi Lake: The largest lake in Yunnan Province",
            "Yuantong Temple: One of the most famous Buddhist temples in Yunnan",
            "Golden Temple (Jindian): A Taoist temple with impressive architecture",
            "Flower and Bird Market: A vibrant market selling flowers, birds, and local crafts",
            "Yunnan Nationalities Village: Showcases the cultures of Yunnan's ethnic minorities"
        ]
        
        self.food = [
            "Crossing-the-Bridge Noodles (Guoqiao Mixian): A famous Yunnan dish with rice noodles in a flavorful broth",
            "Steam Pot Chicken (Qiguo Ji): Tender chicken cooked in a special steamer pot",
            "Erkuai: Rice cakes that can be stir-fried, grilled, or served in soup",
            "Goat Milk Cake (Yangnai Gao): A sweet treat made from goat's milk",
            "Lijiang Baba: A savory pancake filled with various ingredients",
            "Yunnan Coffee: Known for its high quality and unique flavor",
            "Wild Mushroom Hot Pot: Features locally sourced wild mushrooms"
        ]
        
        self.festivals = [
            "Torch Festival: Celebrated by Yi ethnic group with bonfires and traditional dances",
            "Water-Splashing Festival: Dai ethnic group's New Year celebration",
            "Hani New Year: Celebrated by Hani ethnic group with traditional rituals",
            "Yunnan Ethnic Minority Festival: Showcases the cultures of various ethnic groups",
            "Kunming Flower Expo: A grand event showcasing Yunnan's diverse flora"
        ]
        
        self.weather_info = "Kunming has a mild climate year-round, with average temperatures ranging from 15-25°C. It's known as the 'City of Eternal Spring' due to its pleasant weather throughout the year."
        
        self.transportation = "Kunming has a well-developed transportation system including metro, buses, taxis, and共享单车 (shared bikes). The city also has an international airport (Kunming Changshui International Airport) and high-speed rail connections."
    
    def get_response(self, query):
        """Generate response based on user query"""
        query = query.lower()
        
        if any(keyword in query for keyword in ['attraction', 'tourist', 'place', 'visit']):
            return random.choice(self.attractions)
        
        elif any(keyword in query for keyword in ['food', 'dish', 'cuisine', 'eat']):
            return random.choice(self.food)
        
        elif any(keyword in query for keyword in ['festival', 'celebration', 'event']):
            return random.choice(self.festivals)
        
        elif any(keyword in query for keyword in ['weather', 'climate', 'temperature']):
            return self.weather_info
        
        elif any(keyword in query for keyword in ['transport', 'get around', 'bus', 'metro']):
            return self.transportation
        
        elif any(keyword in query for keyword in ['about', 'introduction', 'general']):
            return "Kunming is the capital city of Yunnan Province in China, known as the 'City of Eternal Spring' for its mild climate. It's a city with rich ethnic diversity, beautiful natural scenery, and delicious food."
        
        else:
            return "I can provide information about Kunming's attractions, food, festivals, weather, and transportation. What would you like to know?"

if __name__ == "__main__":
    skill = KunmingSkill()
    print("Kunming City Skill - Type 'exit' to quit")
    while True:
        query = input("Ask about Kunming: ")
        if query.lower() == 'exit':
            break
        response = skill.get_response(query)
        print(f"Response: {response}")
