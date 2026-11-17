import {_WF_} from "/assets/v3/components/workflow.js"
export default {
inject:['ibf'],
data() {return {
    tasks:[], //任务列表
    tags:this.ibf.tags,
    page:{cur:1, max:0}
}},
created(){
    this.query(1);
},
methods:{
query(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var url="/api/tasks?offset="+offset+"&num="+this.ibf.N_PAGE;
    request({method:"GET",url:url}, this.ibf.SERVICE_WF).then(resp=>{
        if(resp.code!=RetCode.OK) {
            return;
        }
        var dt=new Date();
        //flow,did,createAt,step,cmt
        this.tasks=resp.data.tasks.map(t=>{
            dt.setTime(t.createAt);
            t.createAt=datetime2str(dt);
            return t;
        });
        this.page.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    });
},
detail(flow,did) {
    _WF_.showPage(flow, did, this.$router);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="ibf.back"></q-btn>
    <q-toolbar-title>{{tags.home.tasks}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-if="page.max>1">
 <q-pagination color="primary" v-model="page.cur" :max="page.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query" dense></q-pagination>
</div>
<q-list separator>
 <q-item v-for="t in tasks" @click="detail(t.flow,t.did)" clickable>
  <q-item-section>{{t.cmt}}</q-item-section>
  <q-item-section side>
   <q-item-label>{{t.actor}}</q-item-label>
   <q-item-label caption>{{t.createAt}}</q-item-label>
  </q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>
`
}