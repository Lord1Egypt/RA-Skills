export default {
inject:['service', 'tags'],
data() {return {
    state:'ALL',
    stateOpts:[],
    role:'worker',
    services:[], //服务单列表
    cmts:[], //评价
    ctrl:{cur:1,max:0,dlg:false},
    dtl:{},
    myAcc:'',
    score:{val:0,total:0,vBrokerage:0}
}},
created(){
    this.myAcc=this.service.account;
    this.stateOpts=Object.entries(this.tags.service.states).map(
        ([k, v]) => {return {label:v, value:k}});
    this.service.getRole().then(role=>{
        this.role=role;
        this.query(1);
    })
},
methods:{
query(pg) {
    var offset=(parseInt(pg)-1)*this.service.NUM_PER_PAGE;
    var url="/service/myTask?offset="+offset
        +"&num="+this.service.NUM_PER_PAGE+"&state="+this.state;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.services=[];
            this.ctrl.max=0;
        } else {
            this.score.total=resp.data.total;
            this.score.val=resp.data.val;
            this.score.vBrokerage=resp.data.vBrokerage;
            
            this.formatData(resp.data.list, resp.data.cols);
            this.ctrl.max=Math.ceil(resp.data.total/this.service.NUM_PER_PAGE);
        }
    })
},
refresh() {
    this.query(this.ctrl.cur);
},
formatData(rows,cols) {
    var dt=new Date();
    this.services=rows.map(l=>{
        var r={};
        for(var i in cols) {
            r[cols[i]]=l[i];
        }
                   
        dt.setTime(r.createAt*60000);
        r.createAt=datetime2str(dt);
        r.state_s=this.tags.service.states[r.state];
        return r;
    })
},
show_service(id) {
    this.id=id;
    var url="/api/service/get?id="+id
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        var dtl=resp.data;

        var dt=new Date();
        var now=parseInt(dt.getTime()/60000);
        
        dt.setTime(dtl.createAt*60000);
        dtl.id=id;
        dtl.createAt=datetime2str(dt);
        dtl.state_s=this.tags.service.states[dtl.state];
        for(var s of dtl.suppliers) {
            if(s.start<=0) {
                s.start_s=this.tags.service.notStart;
            } else {
                dt.setTime(s.start*60000);
                s.start_s=datetime2str(dt);
            }
            if(s.end<=0) {
                s.end_s=this.tags.service.notEnd;
            } else {
                dt.setTime(s.end*60000);
                s.end_s=datetime2str(dt);
            }
            s.ratio=this.service.formatNum(s.ratio*100,1);
            if(s.start==0)s.interval='0';
            else if(s.end>s.start)s.interval=s.end-s.start;
            else s.interval=now-s.start;
            s.interval+=this.tags.service.unit;
            s.isMy=s.account==this.myAcc;
        }
        this.dtl=dtl;
        this.ctrl.dlg=true;
    })
},
action(start,end) {
    if(end>0)return;
    var url=start==0?"/service/start":"/service/finish";
    request({method:"PUT", url:url, data:{id:this.dtl.id}}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.refresh();
        this.ctrl.dlg=false;
    })
},
load_comments() {
    if(this.cmts.length>0)return;
    var url="/service/comments?service="+this.dtl.id;
    request({method:"GET", url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            return;
        }
        var dt=new Date();
        this.cmts=resp.data.list.map(c=>{
            dt.setTime(c.at);
            c.at=datetime2str(dt);
            return c;
        })
    })
}
},

template:`
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary">
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="service.back"
     v-if="role=='admin'||role=='sales'"></q-btn>
    <q-avatar square v-else><img src="./favicon.png"></q-avatar>
    <q-toolbar-title>{{tags.service.myTask}}</q-toolbar-title>
    <q-btn icon="refresh" flat dense @click="refresh"></q-btn>
    <q-btn flat round dense icon="menu"><q-menu>
     <q-option-group :options="stateOpts" type="radio" v-model="state"
      @update:model-value="query(1)" style="min-width:10em"></q-option-group>
    </q-menu></q-btn>
   </q-toolbar>
   <q-card class="q-mx-sm" flat>
    <q-card-action>
    <q-markup-table flat dark dense style="background:radial-gradient(circle,#33a2ff 0%,#014aaa 100%)">
     <tr>
      <th>{{tags.score.total}}</th>
      <th>{{tags.service.val}}</th>
      <th>{{tags.score.vBrokerage}}</th>
     </tr>
     <tr>
      <td class="text-h6 text-center">{{score.total}}</td>
      <td class="text-h6 text-center">{{score.val}}</td>
      <td class="text-h6 text-center">{{score.vBrokerage}}</td>
     </tr>
    </q-markup-table>
    </q-card-action>
   </q-card>
  </q-header>

  <q-page-container>
    <q-page class="q-pa-md">

<div class="q-pa-lg flex flex-center" v-if="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-markup-table flat>
 <thead><tr>
  <th class="text-left">{{tags.vip.name}}</th>
  <th class="text-right">{{tags.service.val}}</th>
  <th class="text-right">{{tags.creator}}</th>
 </tr></thead>
 <tbody>
 <tr v-for="v in services" style="cursor:pointer;" @click="show_service(v.id)">
  <td class="text-left">
   <div>{{v.name}}</div>
   <div class="text-caption">{{v.code}}</div>
  </td>
  <td class="text-right">
   <div>{{v.val}}</div>
   <div :class="v.state=='OK'?'text-caption':'text-primary'">{{v.state_s}}</div>
  </td>
  <td class="text-right">
   <div>{{v.creator}}</div>
   <div class="text-caption">{{v.createAt}}</div>
  </td>
 </tr>
 </tbody>
</q-markup-table>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.dlg" @hide="cmts=[]">
<q-card style="min-width:80vw;max-width:90vw">
<q-card-section class="row items-center q-pb-none">
  <div class="text-h6">{{dtl.name}}</div>
  <q-space></q-space>
  <q-btn icon="close" flat round dense v-close-popup></q-btn>
</q-card-section>
<q-card-section>
 <q-markup-table style="width:100%;" flat>
  <tr><td>{{tags.vip.code}}</td><td>{{dtl.code}}</td></tr>
  <tr><td>{{tags.creator}}</td><td>{{dtl.creator}}</td></tr>
  <tr><td>{{tags.createAt}}</td><td>{{dtl.createAt}}</td></tr>
  <tr><td>{{tags.service.state}}</td><td :class="dtl.state=='OK'?'':'text-primary'">{{dtl.state_s}}</td></tr>
  <tr><td>{{tags.service.val}}</td><td>{{dtl.val}}</td></tr>
  <tr><td>{{tags.vip.total}}</td><td>{{dtl.total}}</td></tr>
  <tr><td>{{tags.vip.balance}}</td><td>{{dtl.balance}}</td></tr>
  <tr><td>{{tags.cmt}}</td><td>{{dtl.cmt}}</td></tr>
  <tr v-for="s in dtl.suppliers">
   <td>{{s.account}}</td>
   <td>
    <div v-if="!s.isMy||s.start>0">{{s.start_s}}</div>
    <div v-else>
     <q-btn round :label="tags.start" color="orange-9" @click="action(s.start,s.end)"></q-btn>
    </div>
    
    <div v-if="s.isMy&&s.start>0&&s.end==0">
     <q-btn round :label="tags.stop" color="orange-9" @click="action(s.start,s.end)"></q-btn>
    </div>
    <div v-else>{{s.end_s}}</div>
    
    <div class="text-caption">{{tags.service.useTime}}:{{s.interval}}</div>
    <div class="text-caption">{{tags.brokerage.ratio}}:{{s.ratio}}</div>
   </td>
  </tr>
 </q-markup-table>
 
 <q-expansion-item dense dense-toggle expand-separator icon="comment"
  :label="tags.service.cmt" @before-show="load_comments"
  header-class="text-primary">
  <q-markup-table style="width:100%;" flat>
   <tr v-for="c in cmts">
    <td>
     <div class="text-caption">{{c.cmt}}</div>
     <q-rating v-model="c.level" size="1em" color="orange" readonly></q-rating>
     <div class="text-caption">{{c.at_s}}</div>
    </td>
   </tr>
  </q-markup-table>
  <div v-if="cmts.length==0" class="q-pa-md">{{tags.service.noCmt}}</div>
 </q-expansion-item>
</q-card-section>
</q-card>
</q-dialog>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
`
}