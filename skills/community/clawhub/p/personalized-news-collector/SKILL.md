---
name: personalized-news-collector
description: Get current news which matches user's recent interests. It can be triggered when user ask about current news or the events happening around without selecting a specific topic.
---

# Personalized News Collector
  
Analyze user's current interests and collect current news concerning these interests. Finally deliver a report which has categorized the collected news and sort it by popularity.

## Working Process 

### 1. Analyze Interests
All the news conllected news should match user's interests. User's interests can be summarized from recent memory and conversation history. At least **three** main interests should be offered. 

### 2. Collect News

Get news concerning user's interests. You should collect as much as Information from different sources. You can use the command like:
 
``curl -sL `the url of informtion source` ``

You can use the URLs offered at  `sources.md` as your news sources, but some of them may not be available and they should not be your only choices. You are supported to collect Information from more sources, especially when user's interests are not included in `sources.md`. 

### 3.Summary News

After collecting news whose topic matches user's interests, some news may appear in different sources at the same time. Judge the importance of the news based on its frequency of appearance in different sources(if two news items' frequency is the same, judge the importance according to your own opinion), and rank the news in descending order of importance. 

### 4.Output
There should be at least **three** news items for one interest.
Your output should follow the format below:

1. "user's first interest"
	"The news with the highest importance under this interest."
	"The news with the second highest importance under this interest."
	"The news with the third highest importance under this interest."
2. "user's second interest"
	"The news with the highest importance under this interest."
	"The news with the second highest importance under this interest."
	"The news with the third highest importance under this interest."
...........

