"""
domain/state.py - StateRoot immutable aggregate root
"""
from __future__ import annotations
from datetime import datetime
from typing import Dict,List,Optional,Any
from dataclasses import dataclass,field,replace

@dataclass(frozen=True)
class Meta:
    title:str=""; platform:str=""; genre:str=""; created:str=""; updated:str=""; outline:str=""
    @classmethod
    def from_dict(cls,d:dict)->Meta:
        return cls(title=d.get("title",""),platform=d.get("platform",""),genre=d.get("genre",""),created=d.get("created",""),updated=d.get("updated",""),outline=d.get("outline",""))

@dataclass(frozen=True)
class Progress:
    written:int=0; total_planned:int=0; last_chapter:int=0
    def __post_init__(self):
        if self.written<0:raise ValueError(f"written must be >= 0, got {self.written}")
    @classmethod
    def from_dict(cls,d:dict)->Progress:
        # v1.6: 兼容 written 可能是 list 的情况（legacy chapter_transaction 行为）
        w = d.get("written", 0)
        if isinstance(w, list):
            w = len(w)
        elif not isinstance(w, int):
            w = int(w) if w else 0
        return cls(written=w, total_planned=d.get("total_planned",0), last_chapter=d.get("last_chapter",0))

@dataclass(frozen=True)
class Character:
    name:str; identity:str=""; personality:Dict[str,Any]=field(default_factory=dict); state:Dict[str,Any]=field(default_factory=dict); location:str=""; chapters_appeared:List[int]=field(default_factory=list)
    @classmethod
    def from_dict(cls,d:dict)->Character:
        return cls(name=d.get("name",""),identity=d.get("identity",""),personality=d.get("personality",{}),state=d.get("state",{}),location=d.get("location",""),chapters_appeared=list(d.get("chapters_appeared",[])))

@dataclass(frozen=True)
class Hook:
    hook_id:str=""; text:str=""; hook_type:str="general"; status:str="planted"; chapter_planted:int=0; chapter_target:int=0; resolved_at:Optional[int]=None
    @classmethod
    def from_dict(cls,d:dict)->Hook:
        return cls(hook_id=d.get("hook_id",""),text=d.get("text",""),hook_type=d.get("hook_type","general"),status=d.get("status","planted"),chapter_planted=d.get("chapter_planted",0),chapter_target=d.get("chapter_target",0),resolved_at=d.get("resolved_at"))

@dataclass(frozen=True)
class StoryArc:
    name:str=""; description:str=""; start_chapter:int=0; end_chapter:int=0; status:str="planned"
    @classmethod
    def from_dict(cls,d:dict)->StoryArc:
        return cls(name=d.get("name",""),description=d.get("description",""),start_chapter=d.get("start_chapter",0),end_chapter=d.get("end_chapter",0),status=d.get("status","planned"))

@dataclass(frozen=True)
class Plot:
    hooks:List[Hook]=field(default_factory=list); resolved_hooks:List[str]=field(default_factory=list); arcs:List[StoryArc]=field(default_factory=list)
    @classmethod
    def from_dict(cls,d:dict)->Plot:
        return cls(hooks=[Hook.from_dict(h) for h in d.get("hooks",[])],resolved_hooks=list(d.get("resolved_hooks",[])),arcs=[StoryArc.from_dict(a) for a in d.get("arcs",[])])

@dataclass(frozen=True)
class TimelineEntry:
    chapter:int; event:str
    @classmethod
    def from_dict(cls,d:dict)->TimelineEntry:
        return cls(chapter=d["chapter"],event=d["event"])

@dataclass(frozen=True)
class ReaderStats:
    read_rate:float=1.0; sentiment:str="neutral"; warnings:List[str]=field(default_factory=list)
    @classmethod
    def from_dict(cls,d:dict)->ReaderStats:
        return cls(read_rate=d.get("\u9605\u8bfb\u7387",1.0),sentiment=d.get("\u8bc4\u8bba\u60c5\u7eea","neutral"),warnings=list(d.get("\u8b66\u544a",[])))

@dataclass(frozen=True)
class PayoffLedgerEntry:
    id:int; text:str; chapter_planted:int; chapter_fulfilled:Optional[int]=None; fulfilled:bool=False

@dataclass(frozen=True)
class ForeshadowEntry:
    id:str; content:str; chapter_planted:int; chapter_target:Optional[int]=None; status:str="planted"; chapter_revealed:Optional[int]=None
    @classmethod
    def from_dict(cls,d:dict)->ForeshadowEntry:
        return cls(id=d.get("id",""),content=d.get("content",""),chapter_planted=d.get("chapter_planted",0),chapter_target=d.get("chapter_target"),status=d.get("status","planted"),chapter_revealed=d.get("chapter_revealed"))

@dataclass(frozen=True)
class GlobalMemoryEntry:
    chapter:int; summary:str; key_events:List[str]=field(default_factory=list); characters_mentioned:List[str]=field(default_factory=list)
    @classmethod
    def from_dict(cls,d:dict)->GlobalMemoryEntry:
        return cls(chapter=d.get("chapter",0),summary=d.get("summary",""),key_events=list(d.get("key_events",[])),characters_mentioned=list(d.get("characters_mentioned",[])))

@dataclass(frozen=True)
class CharacterStateEntry:
    name:str; location:str=""; emotion:str=""; relationship_to_mc:str=""; last_seen_chapter:int=0
    @classmethod
    def from_dict(cls,d:dict)->CharacterStateEntry:
        return cls(name=d.get("name",""),location=d.get("location",""),emotion=d.get("emotion",""),relationship_to_mc=d.get("relationship_to_mc",""),last_seen_chapter=d.get("last_seen_chapter",0))

@dataclass(frozen=True)
class StateRoot:
    version:str="1.0.0"; concurrency_version:int=0; meta:Meta=field(default_factory=Meta); progress:Progress=field(default_factory=Progress)
    characters:Dict[str,Character]=field(default_factory=dict); settings:List[str]=field(default_factory=list)
    plot:Plot=field(default_factory=Plot); timeline:List[TimelineEntry]=field(default_factory=list)
    readers:ReaderStats=field(default_factory=ReaderStats); foreshadows:List[ForeshadowEntry]=field(default_factory=list)
    character_states:Dict[str,CharacterStateEntry]=field(default_factory=dict)
    global_memory:Dict[int,GlobalMemoryEntry]=field(default_factory=dict)
    payoff_ledger:List[PayoffLedgerEntry]=field(default_factory=list)

    # _KNOWN_KEYS derived from dataclass fields — auto-updates when fields change
    _KNOWN_KEYS = None  # set at class creation time below

    def _bump_version(self) -> "StateRoot":
        """Increment concurrency version (for optimistic locking)."""
        return replace(self, concurrency_version=self.concurrency_version + 1)

    @classmethod
    def default(cls)->StateRoot:
        return cls(meta=Meta(created=datetime.now().isoformat(),updated=datetime.now().isoformat()))

    @classmethod
    def from_dict(cls,d:dict)->StateRoot:
        unknown=set(d.keys())-cls._KNOWN_KEYS
        if unknown:
            import logging; logging.getLogger(__name__).warning("StateRoot.from_dict() dropping %d unknown keys: %s",len(unknown),sorted(unknown))
        return cls(
            version=d.get("version","1.0.0"), concurrency_version=d.get("concurrency_version", 0),
            meta=Meta.from_dict(d.get("meta",{})),
            progress=Progress.from_dict(d.get("progress",{})),
            characters={k:Character.from_dict(v) for k,v in d.get("characters",{}).items()},
            settings=list(d.get("settings",[])), plot=Plot.from_dict(d.get("plot",{})),
            timeline=[TimelineEntry.from_dict(t) for t in d.get("timeline",[])],
            readers=ReaderStats.from_dict(d.get("readers",{})),
            foreshadows=[ForeshadowEntry.from_dict(f) for f in d.get("foreshadows",[])],
            character_states={k:CharacterStateEntry.from_dict(v) for k,v in d.get("character_states",{}).items()},
            global_memory={int(k):GlobalMemoryEntry.from_dict(v) for k,v in d.get("global_memory",{}).items()},
            payoff_ledger=[PayoffLedgerEntry(id=e.get("id",0),text=e.get("text",""),chapter_planted=e.get("chapter_planted",0),chapter_fulfilled=e.get("chapter_fulfilled"),fulfilled=e.get("fulfilled",False)) for e in d.get("payoff_ledger",[])]
        )

    def to_dict(self)->dict:
        return {"version":self.version,"concurrency_version":self.concurrency_version,"meta":{"title":self.meta.title,"platform":self.meta.platform,"genre":self.meta.genre,"created":self.meta.created,"updated":self.meta.updated,"outline":self.meta.outline},"progress":{"written":self.progress.written,"total_planned":self.progress.total_planned,"last_chapter":self.progress.last_chapter},"characters":{k:{"name":v.name,"identity":v.identity,"personality":v.personality,"state":v.state,"location":v.location,"chapters_appeared":v.chapters_appeared} for k,v in self.characters.items()},"settings":self.settings,"plot":{"hooks":[{"hook_id":h.hook_id,"text":h.text,"hook_type":h.hook_type,"status":h.status,"chapter_planted":h.chapter_planted,"chapter_target":h.chapter_target,"resolved_at":h.resolved_at} for h in self.plot.hooks],"resolved_hooks":self.plot.resolved_hooks,"arcs":[{"name":a.name,"description":a.description,"start_chapter":a.start_chapter,"end_chapter":a.end_chapter,"status":a.status} for a in self.plot.arcs]},"timeline":[{"chapter":t.chapter,"event":t.event} for t in self.timeline],"readers":{"\u9605\u8bfb\u7387":self.readers.read_rate,"\u8bc4\u8bba\u60c5\u7eea":self.readers.sentiment,"\u8b66\u544a":self.readers.warnings},"foreshadows":[{"id":f.id,"content":f.content,"chapter_planted":f.chapter_planted,"chapter_target":f.chapter_target,"status":f.status,"chapter_revealed":f.chapter_revealed} for f in self.foreshadows],"character_states":{k:{"name":v.name,"location":v.location,"emotion":v.emotion,"relationship_to_mc":v.relationship_to_mc,"last_seen_chapter":v.last_seen_chapter} for k,v in self.character_states.items()},"global_memory":{str(k):{"chapter":v.chapter,"summary":v.summary,"key_events":v.key_events,"characters_mentioned":v.characters_mentioned} for k,v in self.global_memory.items()},"payoff_ledger":[{"id":e.id,"text":e.text,"chapter_planted":e.chapter_planted,"chapter_fulfilled":e.chapter_fulfilled,"fulfilled":e.fulfilled} for e in self.payoff_ledger]}

    def apply(self,cmd)->tuple:
        from domain.events import ChapterCompletedEvent,CharacterUpdatedEvent,HookAddedEvent,HookResolvedEvent,ForeshadowRegisteredEvent,TimelineUpdatedEvent,ReaderStatsUpdatedEvent
        n=cmd.type
        if n=="write_chapter":return replace(self,progress=replace(self.progress,written=self.progress.written+1)),[ChapterCompletedEvent(chapter=cmd.chapter,text_length=len(cmd.text))]
        if n=="update_character":
            cs=dict(self.characters)
            if cmd.name in cs:cs[cmd.name]=replace(cs[cmd.name],**{k:v for k,v in cmd.updates.items() if hasattr(cs[cmd.name],k)})
            else:cs[cmd.name]=Character(name=cmd.name,**{k:v for k,v in cmd.updates.items() if hasattr(Character(name=""),k)})
            return replace(self,characters=cs),[CharacterUpdatedEvent(name=cmd.name,updates=cmd.updates)]
        if n=="add_hook":
            h=Hook(hook_id=cmd.hook_id,text=cmd.text,hook_type=cmd.hook_type,chapter_planted=cmd.chapter,chapter_target=cmd.chapter_target)
            return replace(self,plot=replace(self.plot,hooks=self.plot.hooks+[h])),[HookAddedEvent(hook_id=cmd.hook_id,chapter=cmd.chapter)]
        if n=="resolve_hook":
            hs=[replace(h,status="resolved",resolved_at=cmd.chapter) if h.hook_id==cmd.hook_id else h for h in self.plot.hooks]
            return replace(self,plot=replace(self.plot,hooks=hs,resolved_hooks=self.plot.resolved_hooks+[cmd.hook_id])),[HookResolvedEvent(hook_id=cmd.hook_id,chapter=cmd.chapter)]
        if n=="add_foreshadow":
            e=ForeshadowEntry(id=cmd.foreshadow_id,content=cmd.content,chapter_planted=cmd.chapter,chapter_target=cmd.chapter_target)
            return replace(self,foreshadows=self.foreshadows+[e]),[ForeshadowRegisteredEvent(foreshadow_id=cmd.foreshadow_id,chapter=cmd.chapter)]
        if n=="update_timeline":return replace(self,timeline=self.timeline+[TimelineEntry(chapter=cmd.chapter,event=cmd.event)]),[TimelineUpdatedEvent(chapter=cmd.chapter,event=cmd.event)]
        if n=="update_readers":
            nr=self.readers
            if cmd.read_rate is not None:nr=replace(nr,read_rate=cmd.read_rate)
            if cmd.sentiment is not None:nr=replace(nr,sentiment=cmd.sentiment)
            return replace(self,readers=nr),[ReaderStatsUpdatedEvent(updates=cmd.updates)]
        if n=="add_warning":
            if cmd.warning in self.readers.warnings:return self,[]
            return replace(self,readers=replace(self.readers,warnings=self.readers.warnings+[cmd.warning])),[]
        import logging; logging.getLogger(__name__).warning(f"StateRoot.apply(): unknown command type '{n}', ignored. Known: write_chapter, update_character, add_hook, resolve_hook, add_foreshadow, update_timeline, update_readers, add_warning")
        return self,[]

# Dynamic _KNOWN_KEYS from dataclass fields
StateRoot._KNOWN_KEYS = frozenset(f.name for f in StateRoot.__dataclass_fields__.values())
