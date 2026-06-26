# LangGraph Usage Library

## OpenAI API Usage
| Description                                                  | File                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Call LLM with OpenAI API (Non-streaming)                     | [openai_call_llm.py](./openai_call_llm.py)                 |
| Call LLM with OpenAI API (Streaming)                         | [openai_call_llm_stream.py](./openai_call_llm_stream.py)   |
| OpenAI API structured output                                 | [openai_structured_output.py](./openai_structured_output.py) |

## LangChain Basic Chat Models
| Description                                                  | File                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Call chat model with LangChain                               | [langchain_chatmodel.py](./langchain_chatmodel.py)         |
| Multiple forms of messages in LangChain                      | [langchain_chatmodel_multi_msg.py](./langchain_chatmodel_multi_msg.py) |
| Simple RAG flow with LangChain                               | [langchain_chatmodel_rag.py](./langchain_chatmodel_rag.py) |
| LangChain chat model with integration tool                   | [langchain_chatmodel_integ_tool.py](./langchain_chatmodel_integ_tool.py) |
| LangChain chat model with custom tool                        | [langchain_chatmodel_custom_tool.py](./langchain_chatmodel_custom_tool.py) |

## LangChain React Agents
| Description                                                  | File                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Call react agent with LangChain                              | [langchain_react_agent.py](./langchain_react_agent.py)     |
| LangChain react agent with integration tool                  | [langchain_react_agent_integ_tool.py](./langchain_react_agent_integ_tool.py) |

## LangGraph Workflows
| Description                                                  | File                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| LangGraph workflow with just one node                        | [langgraph_workflow_one_node.py](./langgraph_workflow_one_node.py) |
| LangGraph workflow running nodes sequentially                | [langgraph_workflow_prompt_chaining.py](./langgraph_workflow_prompt_chaining.py) |
| LangGraph workflow running nodes in parallel and joining results | [langgraph_workflow_parallelization.py](./langgraph_workflow_parallelization.py) |
| LangGraph workflow running nodes with conditional routing    | [langgraph_workflow_routing.py](./langgraph_workflow_routing.py) |
| LangGraph workflow running nodes as an orchestrator and multiple workers | [langgraph_workflow_orch_worker.py](./langgraph_workflow_orch_worker.py) |
| LangGraph workflow running nodes with an evaluator/optimizer | [langgraph_workflow_eval_optim.py](./langgraph_workflow_eval_optim.py) |
| LangGraph workflow with interruption and human feedback      | [langgraph_human_in_the_loop.py](./langgraph_human_in_the_loop.py) |

## LangGraph Memory
| Description                                                  | File                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| LangGraph workflow with short-term memory                    | [langgraph_workflow_st_mem.py](./langgraph_workflow_st_mem.py) |
| LangGraph workflow with long-term memory                     | [langgraph_workflow_lt_mem.py](./langgraph_workflow_lt_mem.py) |

## LangGraph Streaming
| Description                                                  | File                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| LangGraph streaming output                           | [langgraph_streaming.py](./langgraph_streaming.py)         |